import math
import ast

# Your Vector, Point, Plane classes remain the same as you provided.
# I'll include Vector class here for completeness of the processing part.
class Vector:
    def __init__(self, x, y, z):
        """Constructor"""
        self.x = float(x) # Ensure components are floats for calculations
        self.y = float(y)
        self.z = float(z)

    def __str__(self):
        """Outputs this default string when object is printed."""
        # Format to a reasonable number of decimal places if they are floats
        return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

    def modulus(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def add(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def subtract(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def multiply(self, scalar): # Renamed from your code to avoid conflict if 'scalar' is a type
        s = float(scalar)
        return Vector(self.x * s, self.y * s, self.z * s)

    def divide(self, scalar_val): # Renamed from your code
        s = float(scalar_val)
        if s == 0:
            raise ValueError("Cannot divide by zero")
        return Vector(self.x / s, self.y / s, self.z / s)

    def unit_vector(self):
        modulus_self = self.modulus()
        if modulus_self == 0:
            raise ValueError("Zero vector does not have unit vector.")
        return self.divide(modulus_self)

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross_product(self, other):
        return Vector(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.z)

    def angle(self, other):
        dot = self.dot_product(other)
        mod_self = self.modulus()
        mod_other = other.modulus()
        if mod_self == 0 or mod_other == 0:
            raise ValueError("Cannot calculate angle with zero vector.")
        cos_angle = dot / (mod_self * mod_other)
        # Clamp value to avoid domain errors with acos due to potential floating point inaccuracies
        cos_angle = max(-1.0, min(1.0, cos_angle))
        return math.acos(cos_angle)

    def length_of_proj(self, other):
        if other.modulus() == 0:
            raise ValueError("Cannot project onto a zero vector.")
        return self.dot_product(other) / other.modulus()

    def projection_vector(self, other):
        if other.modulus() == 0:
            raise ValueError("Cannot project onto a zero vector.")
        unit_vector_other = other.unit_vector() # Handles zero vector case internally now
        len_proj = self.dot_product(other) / other.modulus() # Corrected projection length calculation
        return unit_vector_other.multiply(len_proj)


    def distance(self, other):
        return (self.subtract(other)).modulus()

class Point:
    def __init__(self, x, y, z):
        """Point is (x, y, z)"""
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):  # displays the following when the object is printed
        return f"({self.x}, {self.y}, {self.z})"

class Plane:
    def __init__(self, a, b, c, d):
        """
        Plane: ax + by + cz = d. Attributes are the coefficients.
        """
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __str__(self):
        """
        Returns a string representation of the plane equation
        e.g. '5x - 7y + 8z = 1'
        """
        return f"{self.a}x + {self.b}y + {self.c}z = {self.d}"

    def on_plane(self, x, y, z):
        """
        Checks whether a given point (x, y, z) lies on the plane and displays output
        """
        if self.a * x + self.b * y + self.c * z == self.d:
          print("Point lies on plane")
        else:
          print("Point does not lie on plane")

    def dist_from_origin(self):
        """
        Returns the distance from the origin to the plane
        """
        return math.sqrt(self.a ** 2 + self.b ** 2 + self.c ** 2)

    def dist_from_pt(self, point):
        """
        Returns the distance from the point to the plane
        """
        numerator = abs(self.a * point.x + self.b * point.y + self.c * point.z - self.d)
        denominator = math.sqrt(self.a ** 2 + self.b ** 2 + self.c ** 2)
        return numerator / denominator


    def angle_plane(self, other_plane):
        """
        Returns the acute angle (in deg, 1 dp) between this plane and another plane
        """
        dot_product = self.a * other_plane.a + self.b * other_plane.b + self.c * other_plane.c
        magnitude1 = math.sqrt(self.a ** 2 + self.b ** 2 + self.c ** 2)
        magnitude2 = math.sqrt(other_plane.a ** 2 + other_plane.b ** 2 + other_plane.c ** 2)
        angle_rad = math.acos(dot_product / (magnitude1 * magnitude2))
        angle_deg = math.degrees(angle_rad)
        return round(min(angle_deg, 180 - angle_deg), 1)

def process_vector_query(input_string):
    output_data = {
        "input_vectors_coords": [], # Store original coords for plotting if needed
        "result_vector_coords": None, # Store result vector coords for plotting
        "scalar_result": None,
        "operation_name": "unknown",
        "display_message": "",
        "error_message": None
    }

    try:
        parsed_input = ast.literal_eval(input_string)
        if not isinstance(parsed_input, list) or len(parsed_input) < 1:
            raise ValueError("Input must be a non-empty list.")

        operation_label = None
        raw_vector_data = []

        if isinstance(parsed_input[-1], str):
            operation_label = parsed_input[-1].lower()
            output_data["operation_name"] = operation_label
            raw_vector_data = parsed_input[:-1]
        else:
            # This case handles if the AI returns only vector(s) without an operation string.
            # Example: "[[1,2,3]]" or "[[1,2,3],[4,5,6]]"
            # We'll treat this as a 'vectors' display operation.
            if all(isinstance(item, list) for item in parsed_input):
                operation_label = "vectors" # Default to displaying vectors
                output_data["operation_name"] = operation_label
                raw_vector_data = parsed_input
            else:
                raise ValueError("Operation must be a string and the last element, or input must be a list of vectors.")


        vector_objs = []
        for v_data in raw_vector_data:
            if not isinstance(v_data, list) or not (2 <= len(v_data) <= 3) : # Allow 2D or 3D vectors
                 # For operations like scalar multiplication: [[1,2,3], 2, 'scalar_multiplication']
                if isinstance(v_data, (int, float)) and operation_label == "scalar_multiplication" and len(raw_vector_data) == 2:
                    # This element is the scalar, already handled if we parse it correctly
                    continue
                raise ValueError(f"Invalid vector format or number of components: {v_data}")
            
            components = [float(comp) for comp in v_data]
            if len(components) == 2: # Handle 2D vector by adding z=0
                components.append(0.0)
            vector_objs.append(Vector(*components))
            output_data["input_vectors_coords"].append(components)


        if not vector_objs and operation_label not in ["scalar_triple_product", "linear_combination", "vector_equation_unknown_lhs"]: # Some ops might have specific parsing
             if not (operation_label == "scalar_multiplication" and len(raw_vector_data) == 2 and isinstance(raw_vector_data[1], (int,float))):
                raise ValueError("No valid vector data found.")

        # --- Handle operations ---
        result = None # To store the computational result
        
        if operation_label == "vector":
            if len(vector_objs) == 1:
                v1 = vector_objs[0]
                output_data["result_vector_coords"] = [v1.x, v1.y, v1.z]
                output_data["display_message"] = f"Vector: {v1}"
            else:
                raise ValueError("Operation 'vector' expects 1 vector.")
        
        elif operation_label == "vectors":
            # For just displaying multiple vectors, no specific 'result' vector beyond the inputs
            output_data["display_message"] = "Displaying input vectors."
            # input_vectors_coords already populated

        elif operation_label == "magnitude":
            if len(vector_objs) == 1:
                v1 = vector_objs[0]
                result = v1.modulus()
                output_data["scalar_result"] = result
                output_data["display_message"] = f"Magnitude of {v1} = {result:.3f}"
            else:
                raise ValueError("Operation 'magnitude' expects 1 vector.")

        elif operation_label == "unit_vector": # Corrected from 'unitvector' for consistency
            if len(vector_objs) == 1:
                v1 = vector_objs[0]
                result_vec = v1.unit_vector()
                output_data["result_vector_coords"] = [result_vec.x, result_vec.y, result_vec.z]
                output_data["display_message"] = f"Unit vector of {v1}: {result_vec}"
            else:
                raise ValueError("Operation 'unit_vector' expects 1 vector.")
        
        # Two-vector operations
        elif operation_label in ["addition", "subtract", "dot_product", "cross_product", "angle", "length_of_proj", "projection_vector", "distance"]:
            if len(vector_objs) == 2:
                v1, v2 = vector_objs
                if operation_label == "addition":
                    result_vec = v1.add(v2)
                    output_data["result_vector_coords"] = [result_vec.x, result_vec.y, result_vec.z]
                    output_data["display_message"] = f"{v1} + {v2} = {result_vec}"
                elif operation_label == "subtract": # Note: your old process_vector_query had 'subtract' not 'subtraction'
                    result_vec = v1.subtract(v2)
                    output_data["result_vector_coords"] = [result_vec.x, result_vec.y, result_vec.z]
                    output_data["display_message"] = f"{v1} - {v2} = {result_vec}"
                elif operation_label == "dot_product": # Note: your old process_vector_query had 'dot product'
                    result = v1.dot_product(v2)
                    output_data["scalar_result"] = result
                    output_data["display_message"] = f"{v1} . {v2} = {result:.3f}"
                elif operation_label == "cross_product":# Note: your old process_vector_query had 'cross product'
                    result_vec = v1.cross_product(v2)
                    output_data["result_vector_coords"] = [result_vec.x, result_vec.y, result_vec.z]
                    output_data["display_message"] = f"{v1} x {v2} = {result_vec}"
                elif operation_label == "angle":
                    result = v1.angle(v2) # result in radians
                    output_data["scalar_result"] = math.degrees(result) # convert to degrees for display
                    output_data["display_message"] = f"Angle between {v1} and {v2}: {output_data['scalar_result']:.2f}°"
                elif operation_label == "length_of_proj": # Note: your old process_vector_query had 'length of projection'
                    result = v1.length_of_proj(v2)
                    output_data["scalar_result"] = result
                    output_data["display_message"] = f"Length of projection of {v1} onto {v2}: {result:.3f}"
                elif operation_label == "projection_vector": # Note: your old process_vector_query had 'projection vector'
                    result_vec = v1.projection_vector(v2)
                    output_data["result_vector_coords"] = [result_vec.x, result_vec.y, result_vec.z]
                    output_data["display_message"] = f"Projection of {v1} onto {v2}: {result_vec}"
                elif operation_label == "distance":
                    result = v1.distance(v2)
                    output_data["scalar_result"] = result
                    output_data["display_message"] = f"Distance between points represented by {v1} and {v2}: {result:.3f}"
            else:
                raise ValueError(f"Operation '{operation_label}' expects 2 vectors.")
        
        # Handling scalar multiplication: e.g., [[1,2,3], 2, 'scalar_multiplication']
        elif operation_label == "scalar_multiplication":
            if len(raw_vector_data) == 2 and isinstance(raw_vector_data[0], list) and isinstance(raw_vector_data[1], (int, float)):
                scalar_val = float(raw_vector_data[1])
                v1 = vector_objs[0] # vector_objs should contain the first element if it was a list
                output_data["input_vectors_coords"] = [[v1.x, v1.y, v1.z]] # ensure input_vectors_coords is set
                result_vec = v1.multiply(scalar_val)
                output_data["result_vector_coords"] = [result_vec.x, result_vec.y, result_vec.z]
                output_data["display_message"] = f"{scalar_val} * {v1} = {result_vec}"
            else:
                raise ValueError("Invalid format for 'scalar_multiplication'. Expected [[vec], scalar, 'op'] or [scalar, [vec], 'op']")


        else: # Fallback for operations not explicitly handled above by name
            output_data["error_message"] = f"Unsupported or unknown operation: '{operation_label}'"
            output_data["display_message"] = output_data["error_message"]
            # No result vector or scalar to set

    except (ValueError, SyntaxError, TypeError) as e:
        output_data["error_message"] = f"Error processing input: {e}. Input: '{input_string}'"
        output_data["display_message"] = output_data["error_message"]
    except ZeroDivisionError as z:
        output_data["error_message"] = f"ZeroDivisionError: {z}. Input: '{input_string}'"
        output_data["display_message"] = output_data["error_message"]
    
    return output_data

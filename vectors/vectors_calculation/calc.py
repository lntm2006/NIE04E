import math

class Vector:
    def __init__(self, x, y, z):
        """Constructor"""
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        """Outputs this default string when object is printed."""
        return f"({self.x}, {self.y}, {self.z})"

    def modulus(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def add(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def subtract(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def multiply(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def divide(self, scalar):
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Vector(self.x / scalar, self.y / scalar, self.z / scalar)

    def unit_vector(self):
        """Returns a unit vector of self"""
        modulus_self = self.modulus()
        if modulus_self == 0:
            raise ValueError("Zero vector does not have unit vector.")
        return self.divide(modulus_self)

    def dot_product(self, other):
        """Calculates dot product of self and other"""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross_product(self, other):
        """Calculates cross product of self and other"""
        return Vector(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.z)

    def angle(self, other):
        """Angle between vectors in radians"""
        dot_product = self.dot_product(other)
        modulus_self = self.modulus()
        modulus_other = other.modulus()
        if modulus_self == 0 or modulus_other == 0:
            raise ValueError("Cannot calculate angle with zero vector.")
        return math.acos(dot_product / (modulus_self * modulus_other))

    def length_of_proj(self, other):
        """Length of the projection of self onto other"""
        return self.dot_product(other) / other.modulus()

    def projection_vector(self, other):
        """Projection vector of self onto other"""
        unit_vector_other = other.unit_vector()
        length_of_proj = self.length_of_proj(unit_vector_other)
        return unit_vector_other.multiply(length_of_proj)

    def distance(self, other):
        """Distance between self and other"""
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

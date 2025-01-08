#Math Generator
import pandas as pd
import numpy as np
import openpyxl

def generate_student_data(num_students=1000):
    """
    Generates synthetic student performance data.
    """

    # Topics and their base difficulty (influences average score)
    topics = {
        'Functions': 0.7, 'Graphs and Transformations': 0.65, 'Equations and Inequalities': 0.7,
        'Sequences and Series': 0.6, 'Vector I': 0.6, 'Vectors II': 0.55, 'Vectors III': 0.5,
        'Complex Number': 0.45, 'Differentiation': 0.6, 'Maclaurin series': 0.5,
        'Integration techniques': 0.55, 'Definite integrals': 0.5, 'Differential equations': 0.45,
        'Probability': 0.7, 'Discrete random variables': 0.6, 'Normal distribution': 0.65,
        'Sampling': 0.6, 'Hypothesis testing': 0.5, 'Correlation and linear regression': 0.55,
        'Class Test 1': 0.7, 'Class Test 2': 0.65, 'Promotional Exam': 0.6,
        'Class Test 3': 0.55, 'Mid-year Exam': 0.5, 'Preliminary Exam': 0.45
    }

    # Student profiles and their distribution
    profiles = {
        'Consistent High': 0.1,
        'Consistent Low': 0.1,
        'Strong Algebra, Weak Calculus': 0.1,
        'Strong Calculus, Weak Stats': 0.1,
        'Strong Vectors, Weak Probability': 0.1,
        'Early Starter': 0.15,
        'Late Bloomer': 0.15,
        'Inconsistent': 0.2
    }

    data = []
    student_id = 1

    for profile, proportion in profiles.items():
        num_students_in_profile = int(num_students * proportion)

        for _ in range(num_students_in_profile):
            student_data = {'Student': f'Student {student_id}'}
            student_id += 1

            # Adjust topic scores based on profile
            for topic, difficulty in topics.items():
                if profile == 'Consistent High':
                    base_score = np.random.normal(85, 5)
                elif profile == 'Consistent Low':
                    base_score = np.random.normal(45, 5)
                elif profile == 'Strong Algebra, Weak Calculus':
                    if topic in ['Functions', 'Graphs and Transformations', 'Equations and Inequalities', 'Sequences and Series', 'Vector I', 'Vectors II']:
                        base_score = np.random.normal(80, 7)
                    else:
                        base_score = np.random.normal(50, 10)
                elif profile == 'Strong Calculus, Weak Stats':
                    if topic in ['Differentiation', 'Maclaurin series', 'Integration techniques', 'Definite integrals', 'Differential equations']:
                        base_score = np.random.normal(80, 7)
                    else:
                        base_score = np.random.normal(50, 10)

                elif profile == 'Strong Vectors, Weak Probability':
                    if topic in ['Vector I', 'Vectors II', 'Vectors III']:
                        base_score = np.random.normal(85, 5)
                    elif topic in ['Probability', 'Discrete random variables', 'Normal distribution']:
                        base_score = np.random.normal(45, 10)
                    else:
                        base_score = np.random.normal(65, 10)

                elif profile == 'Early Starter':
                    if topic in ['Class Test 1', 'Class Test 2', 'Promotional Exam']:
                        base_score = np.random.normal(80, 7)
                    else:
                        base_score = np.random.normal(difficulty * 100, 10) - (topics[topic] * 20 ) # Decrease over time

                elif profile == 'Late Bloomer':
                    if topic in ['Class Test 1', 'Class Test 2', 'Promotional Exam']:
                        base_score = np.random.normal(50, 10)
                    else:
                        base_score = np.random.normal(difficulty * 100, 10) + (topics[topic] * 20 ) # Increase over time

                elif profile == 'Inconsistent':
                    base_score = np.random.normal(60, 15)  # Wider standard deviation

                else:
                    base_score = np.random.normal(difficulty * 100, 10) # Base score based on topic difficulty

                # Add some randomness and ensure scores are within 0-100
                score = int(base_score + np.random.normal(0, 5))
                score = max(0, min(score, 100))
                student_data[topic] = score

            data.append(student_data)

    df = pd.DataFrame(data)
    return df

# Generate data
df = generate_student_data()

# Save to CSV
df.to_csv('student_data.csv', index=False)

# Save to Excel
df.to_excel('student_data.xlsx', index=False)

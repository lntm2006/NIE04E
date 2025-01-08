import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Data Representation and Preprocessing ---

def preprocess_data(data_path):
    """
    Preprocesses the student data from a CSV file.

    Args:
        data_path: Path to the CSV file containing student data.

    Returns:
        A pandas DataFrame ready for clustering.
    """
    df = pd.read_csv(data_path)  # Read data directly from CSV

    # No need for one-hot encoding since all columns are numerical

    # Separate numerical features
    numerical_cols = [col for col in df.columns if col != 'Student']
    numerical_data = df[numerical_cols]

    # Scale numerical features
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numerical_data)
    scaled_df = pd.DataFrame(scaled_data, columns=numerical_cols)

    # Combine back with Student column
    final_df = pd.concat([df['Student'], scaled_df], axis=1)

    return final_df, scaler  # Return scaler for later use with new data
# --- 2. Unsupervised Learning (Clustering) ---

def cluster_students(df, num_clusters=5):
    """
    Clusters students based on their performance data using K-Means.

    Args:
        df: The preprocessed DataFrame.
        num_clusters: The desired number of student clusters.

    Returns:
        The DataFrame with an added 'Cluster' column.
    """
    numerical_df = df.drop('Student', axis=1)  # Remove non-numerical Student column
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    df['Cluster'] = kmeans.fit_predict(numerical_df)
    return df, kmeans  # Return the trained KMeans model
# --- 3. Visualization (PCA) ---

def visualize_clusters(df):
    """
    Visualizes the clusters using PCA for dimensionality reduction.
    """
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(df.drop(['Student', 'Cluster'], axis=1))
    reduced_df = pd.DataFrame(reduced_data, columns=['PCA1', 'PCA2'])
    reduced_df['Cluster'] = df['Cluster']

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='PCA1', y='PCA2', hue='Cluster', data=reduced_df, palette='viridis')
    plt.title('Student Clusters (PCA Visualization)')
    plt.show()
# --- 4. Cluster Analysis and Feedback ---

def analyze_clusters(df):
    """
    Analyzes the characteristics of each cluster and provides feedback,
    including mean, standard deviation, and range.
    """
    topics = df.columns.drop(['Student', 'Cluster'])  # Get the list of topics

    for cluster_num in sorted(df['Cluster'].unique()):
        cluster_data = df[df['Cluster'] == cluster_num]
        print(f"\n--- Cluster {cluster_num} Analysis ---")

        # Calculate mean, standard deviation, and range for each topic
        cluster_means = cluster_data.drop(['Student', 'Cluster'], axis=1).mean()
        cluster_stds = cluster_data.drop(['Student', 'Cluster'], axis=1).std()
        cluster_ranges = (
            cluster_data.drop(['Student', 'Cluster'], axis=1).max()
            - cluster_data.drop(['Student', 'Cluster'], axis=1).min()
        )

        # Print the statistics
        for topic in topics:
            print(f"\n  {topic}:")
            print(f"    Mean: {cluster_means[topic]:.2f}")
            print(f"    Standard Deviation: {cluster_stds[topic]:.2f}")
            print(f"    Range: {cluster_ranges[topic]:.2f}")

        # Example feedback
        for topic in topics:
            if cluster_means[topic] < 0:  # Below average performance (due to scaling)
                print(f"  Students in this cluster could improve on {topic}.")
                if cluster_stds[topic] > 0.8: # Threshold
                    print(f"    Note: There is high variability in {topic} scores within this cluster.")

            if cluster_means[topic] >= 0.5:
                print(f"  Students in this cluster are strong on {topic}.")

        #Identify topics with the highest/lowest standard deviation within a cluster
        highest_std_topic = cluster_stds.idxmax()
        lowest_std_topic = cluster_stds.idxmin()
        print(f"\n  Highest standard deviation in this cluster: {highest_std_topic}")
        print(f"  Lowest standard deviation in this cluster: {lowest_std_topic}")
    # --- 5. Main Program and Workflow ---

def main():
    # Load data
    data_path = 'student_data.csv'
    preprocessed_df, scaler = preprocess_data(data_path)

    # Clustering
    clustered_df, kmeans_model = cluster_students(preprocessed_df.copy())

    # Visualization
    visualize_clusters(clustered_df.copy())

    # Cluster analysis and feedback
    analyze_clusters(clustered_df)

# Function to predict cluster assignment for newer student data
def predict_cluster(new_data_path, scaler, kmeans_model):
    """
    Predicts the cluster assignment for new student data.

    Args:
        new_data_path: Path to the CSV file containing new student data.
        scaler: The StandardScaler object used to preprocess the training data.
        kmeans_model: The trained KMeans model.

    Returns:
        DataFrame with cluster assignments for new data.
    """
    new_df = pd.read_csv(new_data_path)
    new_numerical_data = new_df.drop('Student', axis=1)
    new_scaled_data = scaler.transform(new_numerical_data)  # Use the SAME scaler
    new_scaled_df = pd.DataFrame(new_scaled_data, columns=new_numerical_data.columns)
    new_df['Cluster'] = kmeans_model.predict(new_scaled_df)
    return new_df

# Example usage
# new_clustered_df = predict_cluster('new_student_data.csv', scaler, kmeans_model)
# print(new_clustered_df)

if __name__ == "__main__":
    main()

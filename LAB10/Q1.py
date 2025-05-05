import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score
import os

file_path = r'C:\University\Artificial Intelligence Lab\LAB10\Mall_Customers.csv'

try:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' was not found.")
    df = pd.read_csv(file_path)
except FileNotFoundError as e:
    print(e)
    print("Please ensure 'Mall_Customers.csv' is in 'C:\\University\\Artificial Intelligence Lab\\LAB10'.")
    exit(1)
except Exception as e:
    print(f"An error occurred while loading the dataset: {e}")
    exit(1)

expected_columns = ['Age', 'Annual Income (k$)', 'Spending Score (1-100)']

available_columns = df.columns.tolist()
if not all(col in available_columns for col in expected_columns):
    print(f"Error: The dataset is missing some required columns: {expected_columns}")
    print(f"Available columns in the dataset: {available_columns}")
    print("Please verify the column names in 'Mall_Customers.csv' and update the code accordingly.")
    exit(1)

features_no_scaling = df[expected_columns]

features_scaled = features_no_scaling.copy()
scaler = StandardScaler()
features_scaled[['Annual Income (k$)', 'Spending Score (1-100)']] = scaler.fit_transform(
    features_scaled[['Annual Income (k$)', 'Spending Score (1-100)']]
)

wcss_no_scaling = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(features_no_scaling)
    wcss_no_scaling.append(kmeans.inertia_)
plt.figure()
plt.plot(range(1, 11), wcss_no_scaling, marker='o')
plt.title('Elbow Method without Scaling')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('WCSS')
plt.savefig(r'C:\University\Artificial Intelligence Lab\LAB10\elbow_no_scaling_task1.png')
plt.close()

wcss_scaled = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(features_scaled)
    wcss_scaled.append(kmeans.inertia_)
plt.figure()
plt.plot(range(1, 11), wcss_scaled, marker='o')
plt.title('Elbow Method with Scaling (except Age)')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('WCSS')
plt.savefig(r'C:\University\Artificial Intelligence Lab\LAB10\elbow_scaled_task1.png')
plt.close()

kmeans_no_scaling = KMeans(n_clusters=5, init='k-means++', random_state=42)
clusters_no_scaling = kmeans_no_scaling.fit_predict(features_no_scaling)

kmeans_scaled = KMeans(n_clusters=5, init='k-means++', random_state=42)
clusters_scaled = kmeans_scaled.fit_predict(features_scaled)

pca = PCA(n_components=2)
features_no_scaling_pca = pca.fit_transform(features_no_scaling)
features_scaled_pca = pca.fit_transform(features_scaled)

plt.figure()
plt.scatter(features_no_scaling_pca[:, 0], features_no_scaling_pca[:, 1], c=clusters_no_scaling, cmap='viridis')
plt.title('Clusters without Scaling (PCA)')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.colorbar(label='Cluster')
plt.savefig(r'C:\University\Artificial Intelligence Lab\LAB10\clusters_no_scaling_task1.png')
plt.close()

plt.figure()
plt.scatter(features_scaled_pca[:, 0], features_scaled_pca[:, 1], c=clusters_scaled, cmap='viridis')
plt.title('Clusters with Scaling (except Age) (PCA)')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.colorbar(label='Cluster')
plt.savefig(r'C:\University\Artificial Intelligence Lab\LAB10\clusters_scaled_task1.png')
plt.close()

ari = adjusted_rand_score(clusters_no_scaling, clusters_scaled)
print(f"Adjusted Rand Index: {ari}")

print("Cluster centers without scaling (Age, Annual Income (k$), Spending Score (1-100)):")
print(kmeans_no_scaling.cluster_centers_)
print("Cluster centers with scaling (adjusted for original scale):")
centers_scaled = kmeans_scaled.cluster_centers_.copy()
centers_scaled[:, 1:] = scaler.inverse_transform(centers_scaled[:, 1:])
print(centers_scaled)

print("""
Analysis:
- Without scaling, 'Annual Income (k$)' dominates clustering due to its larger numerical range, leading to clusters primarily based on income levels.
- With scaling (except Age), 'Age' has a disproportionate influence because it retains its original scale, resulting in clusters that emphasize age differences.
- Scaling balances the influence of 'Annual Income (k$)' and 'Spending Score (1-100)', leading to more meaningful segmentation that considers all features more equally.
- The Adjusted Rand Index indicates the similarity between the two clusterings; a low value suggests significant differences due to scaling.
""")
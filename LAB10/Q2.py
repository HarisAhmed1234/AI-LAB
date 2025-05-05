import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

data = {
    'vehicle_serial_no': [5, 3, 8, 2, 4, 7, 6, 10, 1, 9],
    'mileage': [150000, 120000, 250000, 80000, 100000, 220000, 180000, 300000, 75000, 280000],
    'fuel_efficiency': [15, 18, 10, 22, 20, 12, 16, 8, 24, 9],
    'maintenance_cost': [5000, 4000, 7000, 2000, 3000, 6500, 5500, 8000, 1500, 7500],
    'vehicle_type': ['SUV', 'Sedan', 'Truck', 'Hatchback', 'Sedan', 'Truck', 'SUV', 'Truck', 'Hatchback', 'SUV']
}
df = pd.DataFrame(data)

df_encoded = pd.get_dummies(df, columns=['vehicle_type'], drop_first=True)

features = df_encoded.drop('vehicle_serial_no', axis=1)

features_scaled = features.copy()
numerical_features = ['mileage', 'fuel_efficiency', 'maintenance_cost']
scaler = StandardScaler()
features_scaled[numerical_features] = scaler.fit_transform(features[numerical_features])

wcss_no_scaling = []
for i in range(1, 6):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(features)
    wcss_no_scaling.append(kmeans.inertia_)
plt.plot(range(1, 6), wcss_no_scaling)
plt.title('Elbow Method without Scaling')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.savefig('elbow_no_scaling_task2.png')
plt.close()

wcss_scaled = []
for i in range(1, 6):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(features_scaled)
    wcss_scaled.append(kmeans.inertia_)
plt.plot(range(1, 6), wcss_scaled)
plt.title('Elbow Method with Scaling (numerical features)')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.savefig('elbow_scaled_task2.png')
plt.close()

kmeans_no_scaling = KMeans(n_clusters=3, init='k-means++', random_state=42)
clusters_no_scaling = kmeans_no_scaling.fit_predict(features)

kmeans_scaled = KMeans(n_clusters=3, init='k-means++', random_state=42)
clusters_scaled = kmeans_scaled.fit_predict(features_scaled)

df['cluster_no_scaling'] = clusters_no_scaling
df['cluster_scaled'] = clusters_scaled

print(f"Silhouette score without scaling: {silhouette_score(features, clusters_no_scaling)}")
print(f"Silhouette score with scaling: {silhouette_score(features_scaled, clusters_scaled)}")

print("\nCrosstab without scaling:")
print(pd.crosstab(df['vehicle_type'], df['cluster_no_scaling']))
print("\nCrosstab with scaling:")
print(pd.crosstab(df['vehicle_type'], df['cluster_scaled']))

print("""
Without scaling, 'mileage' and 'maintenance_cost' dominate, grouping vehicles by usage intensity.
With scaling, numerical features balance with vehicle types, enhancing type-based segmentation.
""")
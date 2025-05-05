import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
n_students = 100
df = pd.DataFrame({
    'student_id': np.arange(1, n_students + 1),
    'GPA': np.random.uniform(2.0, 4.0, n_students),
    'study_hours': np.random.uniform(5, 20, n_students),
    'attendance_rate': np.random.uniform(60, 100, n_students)
})

features = df[['GPA', 'study_hours', 'attendance_rate']]

scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

wcss = []
for i in range(2, 7):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(features_scaled)
    wcss.append(kmeans.inertia_)
plt.plot(range(2, 7), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.savefig('elbow_task3.png')
plt.close()

kmeans = KMeans(n_clusters=4, init='k-means++', random_state=42)
clusters = kmeans.fit_predict(features_scaled)

df['cluster'] = clusters

plt.scatter(df['study_hours'], df['GPA'], c=df['cluster'])
plt.title('Student Clusters based on Study Hours and GPA')
plt.xlabel('Study Hours')
plt.ylabel('GPA')
plt.savefig('clusters_task3.png')
plt.close()

print(df[['student_id', 'cluster']])
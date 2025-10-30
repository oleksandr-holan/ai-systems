import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

data = {
    "age": [25, 31, 45, 22, 54, 38, 29, 41, 58, 61, 24, 28, 33, 49, 51],
    "income": [50, 75, 120, 35, 150, 90, 60, 110, 180, 200, 45, 65, 80, 130, 160],
    "purchase_score": [85, 80, 20, 95, 25, 75, 90, 30, 15, 10, 88, 92, 78, 22, 18],
}
df = pd.DataFrame(data)

print("--- Original Customer Data ---")
print(df)

scaler = StandardScaler()
scaled_features = scaler.fit_transform(df[["age", "income", "purchase_score"]])
df_scaled = pd.DataFrame(
    scaled_features, columns=["age_scaled", "income_scaled", "purchase_score_scaled"]
)

print("\n--- Scaled Customer Data (for the algorithm) ---")
print(df_scaled.head())

# Within-Cluster Sum of Squares
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init="k-means++", random_state=42, n_init=10)
    kmeans.fit(df_scaled)
    wcss.append(kmeans.inertia_)  # inertia_ is WCSS

plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), wcss, marker="o", linestyle="--")
plt.title("Elbow Method for Optimal k")
plt.xlabel("Number of Clusters (k)")
plt.ylabel("WCSS")
plt.grid(True)

# The plot shows sharp drop from k=1 to k=2, and another significant drop to k=3.
# After k=3, the drop becomes much less pronounced.
# This indicates that k=3 is the optimal number of clusters for our data.
plt.show()

optimal_k = 3
kmeans = KMeans(n_clusters=optimal_k, init="k-means++", random_state=42, n_init=10)

clusters = kmeans.fit_predict(df_scaled)

df["cluster"] = clusters

print("\n--- Customer Data with Assigned Clusters ---")
print(df)

plt.figure(figsize=(12, 8))
sns.scatterplot(
    data=df,
    x="income",
    y="purchase_score",
    hue="cluster",
    palette="viridis",
    s=150,
    alpha=0.8,
    edgecolor="black",
)
plt.title("Customer Segments: Income vs. Purchase Score")
plt.xlabel("Annual Income (in thousands $)")
plt.ylabel("Purchase Score (1-100)")
plt.legend(title="Customer Segment")
plt.grid(True)
plt.show()

cluster_analysis = df.groupby("cluster")[["age", "income", "purchase_score"]].mean()

print("\n--- Analysis of Customer Segments (Mean Values) ---")
print(cluster_analysis)

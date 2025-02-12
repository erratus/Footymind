import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

# Load tracked data
df = pd.read_csv("../data/tracked_players/tracks.csv")

# Extract only positions
positions = df[['xmin', 'ymin']].values  # (x, y) coords of players

# Cluster players into formations
kmeans = KMeans(n_clusters=4, random_state=42).fit(positions)
df['formation_label'] = kmeans.labels_

# Save results
df.to_csv("../results/formations.csv", index=False)
print("Formation clustering completed! Saved in '../results/formations.csv'")

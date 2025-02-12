import pandas as pd
import torch

# Load trained model
model = torch.load("../models/formation_model.pth")
model.eval()

# Load tracked players
df = pd.read_csv("../data/tracked_players/tracks.csv")
positions = df[['xmin', 'ymin']].values

# Convert to tensor
inputs = torch.tensor(positions, dtype=torch.float32)

# Predict formation
predictions = model(inputs).argmax(dim=1)
df['predicted_formation'] = predictions.numpy()

# Save results
df.to_csv("../results/formations.csv", index=False)
print("Predictions saved in '../results/formations.csv'")

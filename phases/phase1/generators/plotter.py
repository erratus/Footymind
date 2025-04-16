import json
import matplotlib.pyplot as plt
import os

# Load your positional data
with open("realistic_90min_position_data.json") as f:
    data = json.load(f)

# Create output folder
os.makedirs("frames", exist_ok=True)

# Generate plots for the first 10 frames
for i in range(1000):
    frame = data[i]
    team_A = frame["players"]["team_A"]
    team_B = frame["players"]["team_B"]
    ball = frame["ball"]

    # Plot setup
    fig, ax = plt.subplots(figsize=(11.8, 7.2))
    ax.set_xlim(0, 1180)
    ax.set_ylim(0, 720)
    ax.set_facecolor("green")
    ax.set_title(f"Frame {frame['frame']} - Timestamp {frame['timestamp']}s")

    # Plot players and ball
    ax.scatter(*zip(*team_A), c="white", edgecolors="black", s=100, label="Team A")
    ax.scatter(*zip(*team_B), c="blue", edgecolors="black", s=100, label="Team B")
    ax.scatter(*ball, c="orange", edgecolors="black", s=80, label="Ball")

    ax.legend(loc="upper right")
    ax.set_aspect('equal')
    plt.tight_layout()

    # Save image
    plt.savefig(f"frames2/frame_{i+1:04d}.png")
    plt.close()

print("First 10 frames saved in the 'frames' folder.")

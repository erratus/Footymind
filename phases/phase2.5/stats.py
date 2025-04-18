import json
import math
from collections import defaultdict

# Load the match event data
with open("../phase2/phase2_event_output1.json", "r") as f:
    match_data = json.load(f)

# Parameters
DISTANCE_THRESHOLD = 50  # pixels
FPS = 50  # Frames per second

# Player stats dictionary
player_stats = defaultdict(lambda: {
    "total_distance": 0,
    "frames_moved": 0,
    "times_manned": 0,
    "goals_scored": 0,
    "passes_done": 0,
    "tackles_done": 0
})

# Track previous player positions
previous_positions = {}

# Loop through each frame
for frame_data in match_data:
    # Movement and manned logic (only if players data exists)
    if "players" in frame_data:
        all_players = []
        for team_key in ["team_A", "team_B"]:
            for idx, (x, y) in enumerate(frame_data["players"].get(team_key, [])):
                player_id = f"Player_{idx+1}_{'A' if team_key == 'team_A' else 'B'}"
                all_players.append({"id": player_id, "x": x, "y": y})

        # Track movement & manned
        for player in all_players:
            player_id = player["id"]
            x, y = player["x"], player["y"]

            # Speed
            if player_id in previous_positions:
                prev_x, prev_y = previous_positions[player_id]
                dist = math.hypot(x - prev_x, y - prev_y)
                player_stats[player_id]["total_distance"] += dist
                player_stats[player_id]["frames_moved"] += 1

            previous_positions[player_id] = (x, y)

            # Manned detection
            for other in all_players:
                if other["id"] != player_id and player_id[-1] != other["id"][-1]:  # Opponent
                    dist = math.hypot(x - other["x"], y - other["y"])
                    if dist < DISTANCE_THRESHOLD:
                        player_stats[player_id]["times_manned"] += 1
                        break

    # Event stats (independent of player positions)
    event = frame_data.get("event")
    by = frame_data.get("by")

    if not event or not by:
        continue

    if event == "pass":
        player_stats[by]["passes_done"] += 1
    elif event == "tackle":
        player_stats[by]["tackles_done"] += 1
    elif event == "goal":
        player_stats[by]["goals_scored"] += 1

# Finalize stats: compute avg_speed
for pid, stats in player_stats.items():
    if stats["frames_moved"] > 0:
        stats["avg_speed"] = round((stats["total_distance"] / stats["frames_moved"]) * FPS, 4)
    else:
        stats["avg_speed"] = 0.0

    # Clean up
    del stats["total_distance"]
    del stats["frames_moved"]

# Save to JSON
with open("player_stats1.json", "w") as f:
    json.dump(player_stats, f, indent=4)

print("✅ Player statistics saved to 'player_stats.json'")

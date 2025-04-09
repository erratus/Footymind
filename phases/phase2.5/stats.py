import json
import math
from collections import defaultdict

# Load the simulated match data
with open("realistic_synthetic_match.json", "r") as f:
    match_data = json.load(f)

# Parameters
DISTANCE_THRESHOLD = 50  # Max distance to count as "manned"
FPS = 50  # Frames per second

# Dictionary to store stats for each player
player_stats = defaultdict(lambda: {
    "total_distance": 0,
    "frames_moved": 0,
    "times_manned": 0,
    "goals_scored": 0,
    "passes_done": 0,
    "tackles_done": 0
})

# Track previous positions of players
previous_positions = {}

# Process match data
for frame_data in match_data:
    if "players" not in frame_data:
        continue  # Skip events-only entries

    players = frame_data["players"]
    ball = frame_data["ball"]

    # Compute movement and manning
    for player in players:
        player_id = player["id"]
        x, y = player["x"], player["y"]

        # Calculate speed
        if player_id in previous_positions:
            prev_x, prev_y = previous_positions[player_id]
            distance_moved = math.sqrt((x - prev_x) ** 2 + (y - prev_y) ** 2)
            player_stats[player_id]["total_distance"] += distance_moved
            player_stats[player_id]["frames_moved"] += 1
        
        previous_positions[player_id] = (x, y)  # Update position

        # Check if the player is manned (close to another player)
        for other_player in players:
            if other_player["id"] != player_id:
                other_x, other_y = other_player["x"], other_player["y"]
                distance = math.sqrt((x - other_x) ** 2 + (y - other_y) ** 2)
                if distance < DISTANCE_THRESHOLD:
                    player_stats[player_id]["times_manned"] += 1
                    break  # Only count one manning per frame

    # Process events
    if "event" in frame_data:
        event = frame_data["event"]
        if event == "pass":
            player_stats[frame_data["player"]]["passes_done"] += 1
        elif event == "tackle":
            # Randomly assign the tackle to a nearby player
            tackled_player = min(players, key=lambda p: math.sqrt((p["x"] - ball["x"])**2 + (p["y"] - ball["y"])**2))
            player_stats[tackled_player["id"]]["tackles_done"] += 1
        elif event in ["home_goal", "opponent_goal"]:
            if ball["owner"]:
                player_stats[ball["owner"]]["goals_scored"] += 1

# Compute final stats
for player_id, stats in player_stats.items():
    if stats["frames_moved"] > 0:
        stats["avg_speed"] = (stats["total_distance"] / stats["frames_moved"]) * FPS
    else:
        stats["avg_speed"] = 0  # Player never moved

    # Remove unnecessary fields
    del stats["total_distance"]
    del stats["frames_moved"]

# Save aggregated data
with open("player_stats.json", "w") as f:
    json.dump(player_stats, f, indent=4)

print("Player statistics saved to 'player_stats.json'.")

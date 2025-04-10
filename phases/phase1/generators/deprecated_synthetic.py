# Re-run after kernel reset

import json
import numpy as np
import random

# Constants
FPS = 50
MATCH_MINUTES = 1
TOTAL_FRAMES = MATCH_MINUTES * 60 * FPS

FIELD_WIDTH = 1180  # pixels
FIELD_HEIGHT = 720  # pixels

NUM_PLAYERS_PER_TEAM = 11

# Utility functions
def random_position():
    return [random.uniform(0, FIELD_WIDTH), random.uniform(0, FIELD_HEIGHT)]

def move_position(pos, max_move=5):
    return [
        min(max(pos[0] + random.uniform(-max_move, max_move), 0), FIELD_WIDTH),
        min(max(pos[1] + random.uniform(-max_move, max_move), 0), FIELD_HEIGHT)
    ]

# Initialize player and ball positions
team_A_players = [random_position() for _ in range(NUM_PLAYERS_PER_TEAM)]
team_B_players = [random_position() for _ in range(NUM_PLAYERS_PER_TEAM)]
ball_position = random_position()

# Initialize events list
event_log = []

# Final dataset
data = []

# Simulate the match frame by frame
for frame in range(TOTAL_FRAMES):
    timestamp = frame / FPS

    # Move players and ball
    team_A_players = [move_position(pos) for pos in team_A_players]
    team_B_players = [move_position(pos) for pos in team_B_players]
    ball_position = move_position(ball_position, max_move=8)

    # Log structured frame data
    frame_data = {
        "timestamp": round(timestamp, 2),
        "frame": frame,
        "players": {
            "team_A": [[round(x, 2), round(y, 2)] for x, y in team_A_players],
            "team_B": [[round(x, 2), round(y, 2)] for x, y in team_B_players]
        },
        "ball": [round(ball_position[0], 2), round(ball_position[1], 2)]
    }

    # Simulate events occasionally (realistic distribution)
    if random.random() < 0.0003:  # goal
        scorer = random.choice(["team_A", "team_B"])
        assist_by = random.randint(0, 10)
        event_log.append({"timestamp": timestamp, "frame": frame, "event": "goal", "team": scorer, "assist_by": assist_by})
    elif random.random() < 0.001:  # pass
        passer = random.choice(["team_A", "team_B"])
        passer_id = random.randint(0, 10)
        event_log.append({"timestamp": timestamp, "frame": frame, "event": "pass", "team": passer, "player": passer_id})
    elif random.random() < 0.0008:  # tackle
        tackler = random.choice(["team_A", "team_B"])
        player_id = random.randint(0, 10)
        event_log.append({"timestamp": timestamp, "frame": frame, "event": "tackle", "team": tackler, "player": player_id})
    elif random.random() < 0.0005:  # foul
        fouler = random.choice(["team_A", "team_B"])
        player_id = random.randint(0, 10)
        event_log.append({"timestamp": timestamp, "frame": frame, "event": "foul", "team": fouler, "player": player_id})
    elif random.random() < 0.001:  # manning (proximity marking)
        marker = random.choice(["team_A", "team_B"])
        player_id = random.randint(0, 10)
        event_log.append({"timestamp": timestamp, "frame": frame, "event": "manning", "team": marker, "player": player_id})

    data.append(frame_data)

# Save the data and event log separately
positional_file = "synthetic_positional_data.json"
event_file = "synthetic_event_log.json"

with open(positional_file, "w") as f:
    json.dump(data, f, indent=2)

with open(event_file, "w") as f:
    json.dump(event_log, f, indent=2)

positional_file, event_file

import json
import numpy as np
import random

# Constants
FPS = 50
MINUTES = 1
SECONDS = MINUTES * 60
TOTAL_FRAMES = FPS * SECONDS

FIELD_WIDTH = 1180
FIELD_HEIGHT = 720
NUM_PLAYERS = 11

# Goal area Y-range (realistic)
GOAL_Y_MIN = FIELD_HEIGHT / 2 - 41
GOAL_Y_MAX = FIELD_HEIGHT / 2 + 41

# Formation & movement
def generate_formation(start_x, team='A'):
    if team == 'A':
        x_offsets = np.linspace(start_x, start_x + 200, 4)
    else:
        x_offsets = np.linspace(start_x + 200, start_x, 4)
    formation = [
        [x_offsets[0], 150], [x_offsets[0], 360], [x_offsets[0], 570],  # Defenders
        [x_offsets[1], 200], [x_offsets[1], 360], [x_offsets[1], 520],  # Midfielders
        [x_offsets[2], 150], [x_offsets[2], 360], [x_offsets[2], 570],  # Forwards
        [x_offsets[3], 100], [x_offsets[3], 620]   # Fullbacks
    ]
    return [[float(round(x, 2)), float(round(y, 2))] for x, y in formation[:NUM_PLAYERS]]

def drift(pos, max_shift=5):
    return [
        min(max(pos[0] + random.uniform(-max_shift, max_shift), 0), FIELD_WIDTH),
        min(max(pos[1] + random.uniform(-max_shift, max_shift), 0), FIELD_HEIGHT)
    ]

# Initialize players and ball
team_A_positions = generate_formation(100, 'A')
team_B_positions = generate_formation(FIELD_WIDTH - 300, 'B')

ball_owner = random.randint(0, NUM_PLAYERS - 1)
ball_team = random.choice(['team_A', 'team_B'])
ball_transition = None  # (frames_left, [start_x, start_y], [end_x, end_y])

frames = []

# Simulate
for frame in range(TOTAL_FRAMES):
    timestamp = round(frame / FPS, 2)

    team_A_positions = [drift(pos) for pos in team_A_positions]
    team_B_positions = [drift(pos) for pos in team_B_positions]

    if ball_transition:
        frames_left, start, end = ball_transition
        t = 1 - frames_left / 15
        ball_position = [
            round(start[0] + (end[0] - start[0]) * t, 2),
            round(start[1] + (end[1] - start[1]) * t, 2)
        ]
        ball_transition = (frames_left - 1, start, end) if frames_left > 1 else None
        if not ball_transition:
            ball_owner = end_owner
            ball_team = end_team
    else:
        ball_position = team_A_positions[ball_owner] if ball_team == 'team_A' else team_B_positions[ball_owner]

    # Occasionally pass the ball
    if random.random() < 0.005 and not ball_transition:
        new_owner = random.randint(0, NUM_PLAYERS - 1)
        new_team = ball_team
        start = team_A_positions[ball_owner] if ball_team == 'team_A' else team_B_positions[ball_owner]
        end = team_A_positions[new_owner] if ball_team == 'team_A' else team_B_positions[new_owner]
        ball_transition = (15, start, end)
        end_owner = new_owner
        end_team = new_team

    # Log frame
    frames.append({
        "timestamp": timestamp,
        "frame": frame,
        "players": {
            "team_A": [[round(x, 2), round(y, 2)] for x, y in team_A_positions],
            "team_B": [[round(x, 2), round(y, 2)] for x, y in team_B_positions]
        },
        "ball": [round(ball_position[0], 2), round(ball_position[1], 2)]
    })

# Save clean tracking data
with open("tracking_data.json", "w") as f:
    json.dump(frames, f, indent=2)

print("✅ Clean 1-minute tracking data saved: clean_1min_tracking_data.json")

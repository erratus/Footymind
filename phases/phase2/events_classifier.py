import json
import math

# Load positional data
with open("phase2_raw_positions.json") as f:
    frames = json.load(f)

def distance(p1, p2):
    return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

def get_closest_player(ball, players, team_name):
    min_dist = float("inf")
    closest_idx = -1
    for idx, (x, y) in enumerate(players):
        d = distance(ball, (x, y))
        if d < min_dist:
            min_dist = d
            closest_idx = idx
    return f"Player_{closest_idx+1}_{team_name}", min_dist

event_output = []
prev_possession = None
prev_ball = None
last_pass = {}

for frame in frames:
    ball = frame["ball"]
    team_A = frame["players"]["team_A"]
    team_B = frame["players"]["team_B"]

    # Find closest players
    player_A, dist_A = get_closest_player(ball, team_A, "A")
    player_B, dist_B = get_closest_player(ball, team_B, "B")

    # Possession logic
    event = None
    by = None
    to = None

    if dist_A < dist_B and dist_A < 40:
        possession = "A"
        by = player_A
    elif dist_B < dist_A and dist_B < 40:
        possession = "B"
        by = player_B
    else:
        possession = None

    # Detect events
    if possession and prev_possession and possession != prev_possession:
        event = "tackle"
        to = by
        by = last_pass.get(prev_possession, None)

    elif possession and possession == prev_possession:
        if prev_ball and distance(ball, prev_ball) > 40:  # Ball moved a lot
            event = "pass"
            to = by
            by = last_pass.get(possession, None)

    if possession:
        last_pass[possession] = by

    # Goal logic
    if ball[0] <= 10 or ball[0] >= 1592:
        event = "goal"
        to = None

    # Save event if detected
    if event:
        event_output.append({
            "timestamp": frame["timestamp"],
            "frame": frame["frame"],
            "ball": ball,
            "event": event,
            "by": by,
            "to": to
        })

    prev_possession = possession
    prev_ball = ball

# Output to JSON
with open("phase2_event_output.json", "w") as f:
    json.dump(event_output, f, indent=4)

print("✅ Event data saved to 'phase2_event_output.json'")
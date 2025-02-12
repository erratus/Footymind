import pandas as pd
from deep_sort_realtime.deepsort_tracker import DeepSort
from detect_players import detect_players  # Import detection function

tracker = DeepSort(max_age=30)

def track_players(image_path):
    detections = detect_players(image_path)
    
    if detections.empty:
        return []

    bbox_xywh = detections[['xmin', 'ymin', 'xmax', 'ymax']].values
    scores = detections['confidence'].values

    tracked_objects = tracker.update_tracks(bbox_xywh, scores)

    player_data = []
    for track in tracked_objects:
        if not track.is_confirmed():
            continue
        player_data.append([track.track_id] + list(track.to_tlbr()))

    return player_data

# Process all frames
import glob

frame_paths = sorted(glob.glob("../data/frames/*.jpg"))
all_tracks = []

for frame in frame_paths:
    tracked_players = track_players(frame)
    for player in tracked_players:
        all_tracks.append([frame] + player)

# Save to CSV
df = pd.DataFrame(all_tracks, columns=["frame", "player_id", "xmin", "ymin", "xmax", "ymax"])
df.to_csv("../data/tracked_players/tracks.csv", index=False)

print("Tracking completed! Saved in '../data/tracked_players/tracks.csv'")

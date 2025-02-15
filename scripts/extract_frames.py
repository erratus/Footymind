import cv2
import numpy as np
import os

def extract_motion_keyframes(video_path, output_dir, motion_threshold=50000):
    """Extracts keyframes from a video based on motion detection."""
    
    # Load video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video: {video_path}")
        return
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    ret, prev_frame = cap.read()
    if not ret:
        print("Error reading first frame")
        return
    
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    frame_count = 0
    keyframe_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Compute absolute difference between frames
        diff = cv2.absdiff(prev_gray, gray)
        motion_score = np.sum(diff)
        
        if motion_score > motion_threshold:
            keyframe_path = os.path.join(output_dir, f"keyframe_{keyframe_count:04d}.jpg")
            cv2.imwrite(keyframe_path, frame)
            keyframe_count += 1
            
        # Update previous frame
        prev_gray = gray.copy()
        frame_count += 1
    
    cap.release()
    print(f"Extracted {keyframe_count} keyframes from {video_path}")

# Example usage
video_file = "./data/soccer_videos/1.mp4"
output_folder = "./data/keyframes/1_720p"
extract_motion_keyframes(video_file, output_folder)

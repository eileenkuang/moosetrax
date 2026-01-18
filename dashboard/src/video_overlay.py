import cv2
import json
import os
import numpy as np

# --- CONFIGURATION ---
# This is where all processed videos will live
OUTPUT_DIR = "data/videos" 

# Standard Colors
COLORS = {
    "red": (0, 0, 255),
    "green": (0, 255, 0),
    "yellow": (0, 255, 255),
    "white": (255, 255, 255),
    "black": (0, 0, 0)
}

# Helper to map AI severity to colors
SEVERITY_MAP = {
    "high": "red",
    "medium": "yellow",
    "low": "green",
    "none": "white"
}

def draw_overlay(frame, text, severity):
    """
    Draws a semi-transparent box with centered text.
    """
    h, w, _ = frame.shape
    color_name = SEVERITY_MAP.get(severity, "white")
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 1.0 
    thickness = 2
    margin = 15
    
    (text_w, text_h), baseline = cv2.getTextSize(text, font, scale, thickness)
    
    x = (w - text_w) // 2
    y = h - 60 
    
    box_p1 = (x - margin, y + baseline + margin)
    box_p2 = (x + text_w + margin, y - text_h - margin)
    
    # Draw Background
    cv2.rectangle(frame, box_p1, box_p2, COLORS["black"], -1)
    
    # Draw Border
    border_color = COLORS.get(color_name, COLORS["white"])
    cv2.rectangle(frame, box_p1, box_p2, border_color, 2)

    # Draw Text
    cv2.putText(frame, text, (x, y), font, scale, COLORS["white"], thickness, cv2.LINE_AA)

def render_annotated_video(input_video_path: str, analysis_data: dict, session_id: str):
    """
    Renders the video and saves it to a predictable path: data/videos/{session_id}.mp4
    Returns the relative filename to be stored in the database.
    """
    
    # 1. Ensure Output Directory Exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 2. Generate Predictable Filename
    # naming convention: session_uuid.mp4
    output_filename = f"{session_id}.mp4"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    print(f"[VIDEO] Processing for Session: {session_id}")
    
    events = analysis_data.get("timeline_events", [])
    
    # UX Fix: Minimum duration
    for event in events:
        if event["end_time"] - event["start_time"] < 2.0:
            event["end_time"] = event["start_time"] + 2.0

    # 3. Handle Video Input
    cap = None
    if input_video_path and os.path.exists(input_video_path):
        cap = cv2.VideoCapture(input_video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    else:
        print("[WARNING] Input video not found. Generating BLACK background.")
        width, height, fps = 1280, 720, 30
        total_frames = 30 * 10 # 10 seconds default

    # 4. Setup Writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_idx = 0
    
    while True:
        if cap:
            ret, frame = cap.read()
            if not ret: break
        else:
            if frame_idx >= total_frames: break
            frame = np.zeros((height, width, 3), dtype=np.uint8)

        current_time = frame_idx / fps
        
        # Check for Events
        active_event = None
        for event in events:
            if event["start_time"] <= current_time <= event["end_time"]:
                active_event = event
                break
        
        if active_event:
            # Map severity to color automatically
            severity = active_event.get("severity", "low")
            draw_overlay(frame, active_event["overlay_text"], severity)

        out.write(frame)
        frame_idx += 1

    if cap: cap.release()
    out.release()
    
    print(f"[SUCCESS] Video saved to: {output_path}")
    
    # Return JUST the filename (or relative path) for the database
    return output_filename
import cv2
import mediapipe as mp
import numpy as np
import time
from ultralytics import YOLO
import pandas as pd
from datetime import datetime

# --- SETUP ---
# Load the YOLOv8 model
model = YOLO('yolov8n.pt')
unauthorized_objects = ['cell phone', 'book']

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh

# Initialize Webcam
cap = cv2.VideoCapture(0)

# --- STATE VARIABLES ---
# Event Log
event_log = []
last_event_type = None
last_event_time = time.time()

# Timers
focus_lost_start_time = None
FOCUS_LOST_THRESHOLD = 5

no_face_start_time = None
NO_FACE_THRESHOLD = 10

# Interview Start Time
interview_start_time = time.time()
CANDIDATE_NAME = "Aniket Singh" # Sample Name

def log_event(event_type):
    """Logs an event only if it's a new type or has been some time since the last."""
    global last_event_type, last_event_time, event_log
    current_time = time.time()
    # Log only if event type is new or 5 seconds have passed since the last same event
    if event_type != last_event_type or (current_time - last_event_time) > 5:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event_log.append({'timestamp': timestamp, 'event': event_type})
        last_event_type = event_type
        last_event_time = current_time
        print(f"Logged Event: {event_type}") # For debugging

# --- MAIN LOOP ---
with mp_face_mesh.FaceMesh(max_num_faces=2, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # --- Object Detection ---
        yolo_results = model(frame, stream=True, verbose=False)
        for r in yolo_results:
            for box in r.boxes:
                cls = int(box.cls[0])
                class_name = model.names[cls]
                if class_name in unauthorized_objects:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(frame, f"UNAUTHORIZED ITEM: {class_name}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    log_event(f"Unauthorized Item: {class_name}")

        # --- Face & Focus Detection ---
        frame_h, frame_w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            no_face_start_time = None
            if len(results.multi_face_landmarks) > 1:
                cv2.putText(frame, "MULTIPLE FACES DETECTED", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                log_event("Multiple Faces Detected")
            else:
                # Gaze Detection Logic
                face_landmarks = results.multi_face_landmarks[0]
                nose_2d = (int(face_landmarks.landmark[1].x * frame_w), int(face_landmarks.landmark[1].y * frame_h))
                left_eye_2d = (int(face_landmarks.landmark[33].x * frame_w), int(face_landmarks.landmark[33].y * frame_h))
                right_eye_2d = (int(face_landmarks.landmark[263].x * frame_w), int(face_landmarks.landmark[263].y * frame_h))
                dist_left = nose_2d[0] - left_eye_2d[0]
                dist_right = right_eye_2d[0] - nose_2d[0]
                if dist_left > dist_right * 1.2: gaze_direction = "RIGHT"
                elif dist_right > dist_left * 1.2: gaze_direction = "LEFT"
                else: gaze_direction = "CENTER"
                
                if gaze_direction != "CENTER":
                    if focus_lost_start_time is None: focus_lost_start_time = time.time()
                    elif time.time() - focus_lost_start_time > FOCUS_LOST_THRESHOLD:
                        cv2.putText(frame, "USER LOOKING AWAY", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        log_event("User Looking Away")
                else:
                    focus_lost_start_time = None
        else:
            focus_lost_start_time = None
            if no_face_start_time is None: no_face_start_time = time.time()
            elif time.time() - no_face_start_time > NO_FACE_THRESHOLD:
                cv2.putText(frame, "NO FACE DETECTED", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                log_event("No Face Detected")
        
        cv2.imshow('Proctoring System', frame)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

# --- AFTER LOOP (GENERATE REPORT) ---
cap.release()
cv2.destroyAllWindows()

interview_end_time = time.time()
interview_duration = round(interview_end_time - interview_start_time)

# Calculate counts
focus_lost_count = sum(1 for event in event_log if "Looking Away" in event['event'])
suspicious_events = [event for event in event_log if "Looking Away" not in event['event']]
suspicious_events_count = len(suspicious_events)

# Calculate Integrity Score
score = 100
score -= focus_lost_count * 5 # -5 for each time focus is lost
score -= suspicious_events_count * 10 # -10 for other major events
final_score = max(0, score) # Score cannot be negative

# Create Report Data
report_data = {
    'Candidate Name': [CANDIDATE_NAME],
    'Interview Duration (seconds)': [interview_duration],
    'Number of times focus lost': [focus_lost_count],
    'Suspicious Events Count': [suspicious_events_count],
    'Final Integrity Score': [f"{final_score}/100"]
}

# Create a DataFrame for the summary
summary_df = pd.DataFrame(report_data)

# Create a DataFrame for the detailed event log
log_df = pd.DataFrame(event_log)

# Save to a single CSV file
report_filename = "proctoring_report.csv"
with open(report_filename, 'w') as f:
    summary_df.to_csv(f, index=False)
    f.write('\n') # Add a newline for separation
    log_df.to_csv(f, index=False)

print(f"\nInterview finished. Proctoring report generated: {report_filename}")
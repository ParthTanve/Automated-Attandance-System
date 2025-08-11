import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime
from face_manager import load_known_faces  # Loads known encodings and names

ATTENDANCE_FILE = "attendance.csv"

def mark_attendance(name):
    """
    Marks attendance in a CSV file with name, date, and time.
    Avoids duplicate entries for the same person on the same day.
    """
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # Create file if not exists
    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, 'w') as f:
            f.write("Name,Date,Time\n")

    # Read existing attendance
    with open(ATTENDANCE_FILE, 'r+') as f:
        lines = f.readlines()
        names_today = [line.split(',')[0] for line in lines if date_str in line]

        if name not in names_today:
            f.write(f"{name},{date_str},{time_str}\n")
            print(f"[INFO] Attendance marked for {name} at {time_str} on {date_str}")


def run_attendance():
    """
    Runs the attendance system using webcam feed.
    """
    known_encodings, known_names = load_known_faces()

    print("[INFO] Starting camera...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[ERROR] Could not access the camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to grab frame.")
            break

        # Resize for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect faces & encode
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                match_index = matches.index(True)
                name = known_names[match_index]
                mark_attendance(name)

            # Draw label
            y1, x2, y2, x1 = [v * 4 for v in face_locations[0]]  # Scale back up
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, name, (x1 + 6, y2 - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Attendance System", frame)

        # Quit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Attendance system stopped.")

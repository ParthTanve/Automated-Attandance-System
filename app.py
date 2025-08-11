import cv2
import face_recognition
import os
import sqlite3
from datetime import datetime
from PIL import Image

# Folder to store registered faces
KNOWN_FACES_DIR = "known_faces"
# Database file
DB_PATH = "attendance.db"


# ==============================
# Database Initialization
# ==============================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    name TEXT,
                    date TEXT,
                    time TEXT
                )''')
    conn.commit()
    conn.close()


# ==============================
# Convert all images to 8-bit RGB
# ==============================
def convert_to_rgb_images(folder):
    for filename in os.listdir(folder):
        if filename.lower().endswith(".jpg"):
            path = os.path.join(folder, filename)
            try:
                img = Image.open(path).convert("RGB")
                img.save(path, format="JPEG")
                print(f"[INFO] Converted {filename} to RGB format.")
            except Exception as e:
                print(f"[ERROR] Failed to convert {filename}: {e}")


# ==============================
# Load Known Faces
# ==============================
def load_known_faces():
    known_encodings = []
    known_names = []

    if not os.path.exists(KNOWN_FACES_DIR):
        os.makedirs(KNOWN_FACES_DIR)

    convert_to_rgb_images(KNOWN_FACES_DIR)

    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.lower().endswith(".jpg"):
            path = os.path.join(KNOWN_FACES_DIR, filename)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if len(encodings) > 0:
                known_encodings.append(encodings[0])
                known_names.append(os.path.splitext(filename)[0])
                print(f"[INFO] Loaded {filename}")
            else:
                print(f"[WARNING] No face found in {filename}")
    return known_encodings, known_names


# ==============================
# Mark Attendance
# ==============================
def mark_attendance(name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    c.execute("SELECT * FROM attendance WHERE name=? AND date=?", (name, date))
    result = c.fetchone()
    if not result:
        c.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)", (name, date, time))
        conn.commit()
        print(f"[INFO] Attendance marked for {name}")
    conn.close()


# ==============================
# Register New Face
# ==============================
def register_new_face():
    name = input("Enter name to register: ").strip()
    if not name:
        print("[ERROR] Name cannot be empty.")
        return

    cam = cv2.VideoCapture(0)
    print("[INFO] Press 'c' to capture image.")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("[ERROR] Failed to access camera.")
            break

        cv2.imshow("Register Face", frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            img_path = os.path.join(KNOWN_FACES_DIR, f"{name}.jpg")
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb).convert("RGB")  # Ensure 8-bit RGB
            img.save(img_path, format="JPEG")
            print(f"[INFO] Registered face for {name}")
            break

    cam.release()
    cv2.destroyAllWindows()


# ==============================
# Attendance System
# ==============================
def run_attendance():
    known_encodings, known_names = load_known_faces()
    if not known_encodings:
        print("[ERROR] No known faces found. Please register first.")
        return

    cam = cv2.VideoCapture(0)
    print("[INFO] Running attendance. Press 'q' to quit.")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("[ERROR] Camera not accessible.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            name = "Unknown"

            if len(known_encodings) > 0:
                matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
                face_distances = face_recognition.face_distance(known_encodings, face_encoding)

                if True in matches:
                    best_match_index = min(range(len(face_distances)), key=face_distances.__getitem__)
                    name = known_names[best_match_index]
                    mark_attendance(name)

            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow("Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


# ==============================
# Main Menu
# ==============================
def main():
    init_db()
    while True:
        print("\n1. Register New Face\n2. Start Attendance\n3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            register_new_face()
        elif choice == '2':
            run_attendance()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()

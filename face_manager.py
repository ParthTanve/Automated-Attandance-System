import os
import face_recognition
from image_utils import convert_to_rgb_images

KNOWN_FACES_DIR = "known_faces"

# Create the folder if it does not exist
if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

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
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(os.path.splitext(filename)[0])
                print(f"[INFO] Loaded {filename}")
            else:
                print(f"[WARNING] No face found in {filename}")
    return known_encodings, known_names

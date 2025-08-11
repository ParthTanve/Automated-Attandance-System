import cv2
import os
from PIL import Image
from face_manager import KNOWN_FACES_DIR

def register_new_face():
    name = input("Enter name to register: ").strip()
    if not name:
        print("[ERROR] Name cannot be empty.")
        return

    if not os.path.exists(KNOWN_FACES_DIR):
        os.makedirs(KNOWN_FACES_DIR)

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
            img = Image.fromarray(rgb).convert("RGB")
            img.save(img_path, format="JPEG")
            print(f"[INFO] Registered face for {name}")
            break

    cam.release()
    cv2.destroyAllWindows()

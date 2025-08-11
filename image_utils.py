import cv2
import os

def convert_to_rgb_images(input_folder, output_folder):
    """
    Converts all JPG images in a folder to RGB format and saves them in output_folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".jpg"):
            img_path = os.path.join(input_folder, filename)
            image = cv2.imread(img_path)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR))
            print(f"Converted {filename} to RGB and saved to {output_path}")

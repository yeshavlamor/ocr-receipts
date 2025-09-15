# this script contains preprocessing functions to prepare images for ocr 
import os
import cv2
import numpy as np
from PIL import Image
from utils import heic2png 

# preprocessing techniques
def set_image_dpi(file_path):
    img = Image.open(file_path)
    length_x, width_y = img.size
    factor = min(1, float(1024.0 / lengtx))
    size = int(factor * length_x), int(factor * width_y)
    img_resized = img.resize(size, Image.LANCZOS)
    return np.array(img_resized)

def denoise(img):
    return cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

def binarise(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary_img

# function that combines all preprocessing techniques
def preprocess_images(source_folder, target_folder, output_folder):
    heic2png(source_folder, target_folder)
    files = os.listdir(target_folder)
    counter = 0

    for file in files:
        image_path = os.path.join(target_folder, file)
        new_file_name = f"preprocessed_{str(counter).zfill(2)}.png"
        new_image_path = os.path.join(output_folder, new_file_name)

        if not os.path.exists(new_image_path):
            img_pil = Image.open(image_path).convert('RGB')
            img = np.array(img_pil)

            if img is None:
                print(f"Error loading image {image_path}")
                continue

            resized_img = set_image_dpi(image_path)
            denoised_img = denoise(resized_img)
            binarised_img = binarise(denoised_img)

            cv2.imwrite(new_image_path, binarised_img)
            print(f"Processed: {file}, New path: {new_image_path}")
        else:
            print(f"File already exists: {new_image_path}")

        counter += 1
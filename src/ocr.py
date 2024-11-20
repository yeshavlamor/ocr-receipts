# this script contains all ocr text extraction functions 
from PIL import Image
import pytesseract
import os

# use pytesseract ocr engine to extract text 
def perform_ocr(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang='eng+tha')
    return text 

# do ocr on all images 
def process_all_images(preprocessed_folder, files, results):
    for file in files:
        image_path = os.path.join(preprocessed_folder, file)
        if not os.path.exists(image_path):
            print(f"Error. Image {file} does not exist.")
            continue 

        text = perform_ocr(image_path)
        results.append({'file': file, 'text': text})

    return results 
    


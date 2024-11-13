import os 
from wand.image import Image

def heic2png(source_folder, target_folder):
    # create the target folder if it doesn't exist
    os.makedirs(target_folder, exist_ok=True)

    for file in os.listdir(source_folder):
        if file.lower().endswith('.heic'):
            source_file = os.path.join(source_folder, file)
            target_file = os.path.join(target_folder, file.replace(".HEIC", ".PNG").replace(".heic", ".png"))

            # check if target file already exists
            if not os.path.exists(target_file):
              with Image(filename=source_file) as img:
                  img.format = 'png'
                  img.save(filename=target_file)

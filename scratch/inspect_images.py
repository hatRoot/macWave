import os
from PIL import Image

images_dir = '/Users/joelduran/Documents/GitHub/MacWaveT2/images'
for filename in os.listdir(images_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        filepath = os.path.join(images_dir, filename)
        try:
            with Image.open(filepath) as img:
                print(f"{filename}: format={img.format}, size={img.size}, mode={img.mode}")
        except Exception as e:
            print(f"{filename}: Error {e}")

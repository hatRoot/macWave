import os
from PIL import Image

filepath = '/Users/joelduran/.gemini/antigravity-ide/brain/46c324bb-c2f1-4bbb-83c2-7a1eaae959f2/media__1780008917038.png'
with Image.open(filepath) as img:
    alpha = img.split()[-1]
    bbox = alpha.getbbox()
    print(f"Bounding box of alpha channel: {bbox}")

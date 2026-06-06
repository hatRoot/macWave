import os
from PIL import Image

filepath = '/Users/joelduran/.gemini/antigravity-ide/brain/46c324bb-c2f1-4bbb-83c2-7a1eaae959f2/media__1780008917038.png'
with Image.open(filepath) as img:
    print(f"Format: {img.format}")
    print(f"Size: {img.size}")
    print(f"Mode: {img.mode}")
    # Get pixel data sample
    pixels = list(img.getdata())
    print(f"Total pixels: {len(pixels)}")
    non_transparent = sum(1 for p in pixels if len(p) < 4 or p[3] > 0)
    print(f"Non-transparent pixels: {non_transparent}")
    
    # Calculate bounds of non-white (or non-black if it's on a black background) pixels
    # Let's count colors
    colors = img.getcolors(maxcolors=1000000)
    if colors:
        print(f"Unique colors: {len(colors)}")
        # Sort colors by frequency
        colors.sort(reverse=True)
        print("Top 10 colors (count, color):")
        for count, color in colors[:10]:
            print(f"  {count}: {color}")
            
    # Bounding box of non-white pixels
    gray = img.convert('L')
    import PIL.ImageOps as ImageOps
    # Find bounding box of dark pixels (less than 200)
    inverted = ImageOps.invert(gray)
    bbox = inverted.getbbox()
    print(f"Bounding box (inverted): {bbox}")

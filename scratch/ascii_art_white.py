import os
from PIL import Image

def ascii_art(filepath, cols=80):
    try:
        img = Image.open(filepath)
        img = img.convert('L')
        width, height = img.size
        aspect_ratio = height / width
        new_width = cols
        new_height = int(new_width * aspect_ratio * 0.5)
        img = img.resize((new_width, new_height))
        chars = "@%#*+=-:. "
        num_chars = len(chars)
        ascii_str = []
        for y in range(new_height):
            line = []
            for x in range(new_width):
                pixel = img.getpixel((x, y))
                idx = int((pixel / 255.0) * (num_chars - 1))
                line.append(chars[idx])
            ascii_str.append("".join(line))
        return "\n".join(ascii_str)
    except Exception as e:
        return f"Error: {e}"

images_dir = '/Users/joelduran/Documents/GitHub/MacWaveT2/images'
print("--- logo_wave_white.png ---")
print(ascii_art(os.path.join(images_dir, 'logo_wave_white.png')))
print("--- logo_dashboard_white.png ---")
print(ascii_art(os.path.join(images_dir, 'logo_dashboard_white.png')))

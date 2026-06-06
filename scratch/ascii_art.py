import os
from PIL import Image

def ascii_art(filepath, cols=80):
    try:
        img = Image.open(filepath)
        # Convert to grayscale
        img = img.convert('L')
        # Calculate aspect ratio
        width, height = img.size
        aspect_ratio = height / width
        new_width = cols
        new_height = int(new_width * aspect_ratio * 0.5) # 0.5 because font characters are taller than wide
        img = img.resize((new_width, new_height))
        
        # Ascii characters from dark to light
        chars = "@%#*+=-:. "
        num_chars = len(chars)
        
        ascii_str = []
        for y in range(new_height):
            line = []
            for x in range(new_width):
                pixel = img.getpixel((x, y))
                # Map pixel (0-255) to character index (0 to num_chars-1)
                idx = int((pixel / 255.0) * (num_chars - 1))
                line.append(chars[idx])
            ascii_str.append("".join(line))
        return "\n".join(ascii_str)
    except Exception as e:
        return f"Error: {e}"

images_dir = '/Users/joelduran/Documents/GitHub/MacWaveT2/images'
print("--- negro.png ---")
print(ascii_art(os.path.join(images_dir, 'negro.png')))

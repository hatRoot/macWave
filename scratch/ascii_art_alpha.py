import os
from PIL import Image

def ascii_art_alpha(filepath, cols=80):
    try:
        img = Image.open(filepath)
        # Get alpha channel
        alpha = img.split()[-1]
        width, height = alpha.size
        aspect_ratio = height / width
        new_width = cols
        new_height = int(new_width * aspect_ratio * 0.5)
        alpha = alpha.resize((new_width, new_height))
        
        # Ascii characters from transparent (light) to opaque (dark)
        # We invert because transparent is white (background) and opaque is black (foreground)
        chars = " .:-=+*#%@"
        num_chars = len(chars)
        
        ascii_str = []
        for y in range(new_height):
            line = []
            for x in range(new_width):
                pixel = alpha.getpixel((x, y))
                # Map pixel (0-255) to character index
                idx = int((pixel / 255.0) * (num_chars - 1))
                line.append(chars[idx])
            ascii_str.append("".join(line))
        return "\n".join(ascii_str)
    except Exception as e:
        return f"Error: {e}"

input_path = '/Users/joelduran/.gemini/antigravity-ide/brain/46c324bb-c2f1-4bbb-83c2-7a1eaae959f2/media__1780008917038.png'
print(ascii_art_alpha(input_path, cols=70))

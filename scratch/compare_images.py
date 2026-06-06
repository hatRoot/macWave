import os
from PIL import Image, ImageOps

images_dir = '/Users/joelduran/Documents/GitHub/MacWaveT2/images'
target_images = ['negro.png', 'logo_dashboard_white.png', 'logo_wave_white.png', '1.png', '2.png', '3.png']

for filename in target_images:
    filepath = os.path.join(images_dir, filename)
    if os.path.exists(filepath):
        try:
            with Image.open(filepath) as img:
                # Check if it has transparency or is grayscale/RGB
                # Convert to grayscale to check brightness
                gray = img.convert('L')
                extrema = gray.getextrema()
                # Count black vs white pixels (threshold at 128)
                pixels = list(gray.getdata())
                black_pixels = sum(1 for p in pixels if p < 128)
                white_pixels = sum(1 for p in pixels if p >= 128)
                pct_black = (black_pixels / len(pixels)) * 100
                bbox = gray.getbbox()
                print(f"{filename}: size={img.size}, mode={img.mode}, format={img.format}, black_pixels={pct_black:.1f}%, bbox={bbox}")
        except Exception as e:
            print(f"{filename}: Error: {e}")
    else:
        print(f"{filename}: Does not exist")

import os
from PIL import Image

def crop_logo():
    images_dir = '/Users/joelduran/Documents/GitHub/MacWaveT2/images'
    
    # Process negro.png
    negro_path = os.path.join(images_dir, 'negro.png')
    with Image.open(negro_path) as img:
        width, height = img.size
        # The text is in the bottom ~30% of the image. Let's crop the top 70%.
        icon_img = img.crop((0, 0, width, int(height * 0.70)))
        
        # Get bounding box of non-transparent/non-white pixels to tight crop
        # Convert to grayscale and invert to find bounding box of content
        alpha = icon_img.split()[-1] if img.mode == 'RGBA' else None
        if alpha:
            bbox = alpha.getbbox()
        else:
            gray = icon_img.convert('L')
            # Assuming white background, invert to find bounding box of black pixels
            inverted = ImageOps.invert(gray)
            bbox = inverted.getbbox()
            
        if bbox:
            # Add some padding around the cropped icon (e.g., 20 pixels)
            pad = 20
            left = max(0, bbox[0] - pad)
            top = max(0, bbox[1] - pad)
            right = min(width, bbox[2] + pad)
            bottom = min(int(height * 0.70), bbox[3] + pad)
            
            cropped_icon = icon_img.crop((left, top, right, bottom))
            cropped_icon.save(os.path.join(images_dir, 'negro_cropped.png'))
            print("Cropped negro.png successfully!")
        else:
            print("Could not find bounding box for negro.png")

    # Process logo_dashboard_white.png
    white_path = os.path.join(images_dir, 'logo_dashboard_white.png')
    if os.path.exists(white_path):
        with Image.open(white_path) as img:
            width, height = img.size
            icon_img = img.crop((0, 0, width, int(height * 0.70)))
            
            alpha = icon_img.split()[-1] if img.mode == 'RGBA' else None
            if alpha:
                bbox = alpha.getbbox()
            else:
                gray = icon_img.convert('L')
                bbox = gray.getbbox()
                
            if bbox:
                pad = 20
                left = max(0, bbox[0] - pad)
                top = max(0, bbox[1] - pad)
                right = min(width, bbox[2] + pad)
                bottom = min(int(height * 0.70), bbox[3] + pad)
                
                cropped_icon = icon_img.crop((left, top, right, bottom))
                cropped_icon.save(os.path.join(images_dir, 'logo_dashboard_white_cropped.png'))
                print("Cropped logo_dashboard_white.png successfully!")
            else:
                print("Could not find bounding box for logo_dashboard_white.png")

if __name__ == '__main__':
    crop_logo()

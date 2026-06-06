import os
from PIL import Image, ImageOps

def process_logos():
    # Paths
    input_path = '/Users/joelduran/.gemini/antigravity-ide/brain/46c324bb-c2f1-4bbb-83c2-7a1eaae959f2/media__1780008917038.png'
    output_negro = '/Users/joelduran/Documents/GitHub/MacWaveT2/images/negro.png'
    output_white = '/Users/joelduran/Documents/GitHub/MacWaveT2/images/logo_dashboard_white.png'
    output_wave_white = '/Users/joelduran/Documents/GitHub/MacWaveT2/images/logo_wave_white.png'
    
    # Load original image
    img = Image.open(input_path).convert('RGBA')
    width, height = img.size
    
    # Let's create a transparent version first (Light background version)
    # We will make any pixel that is very close to white transparent.
    # To avoid creating holes inside the logo, we can use floodfill or just a threshold.
    # Actually, let's look at the logo: it has no pure white regions inside it that should not be transparent,
    # except maybe very tiny specular highlights. Let's test a simple threshold: if R > 245 and G > 245 and B > 245, set alpha = 0.
    
    data = img.getdata()
    newData = []
    for item in data:
        # If the pixel is very close to white, make it transparent
        if item[0] > 248 and item[1] > 248 and item[2] > 248:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    
    img_transparent = Image.new('RGBA', img.size)
    img_transparent.putdata(newData)
    
    # Save the light theme version as negro.png
    img_transparent.save(output_negro, 'PNG')
    print(f"Saved light theme logo to {output_negro}")
    
    # Now let's create the dark theme version (White logo).
    # For this, we want the dark text and dark metallic outlines to be white/light.
    # Let's look at pixels in the transparent image:
    # If the pixel is not transparent (alpha > 0):
    #   We can convert dark pixels (e.g. R < 100, G < 100, B < 100) to white/light gray
    #   We want to keep the beautiful blue glow! The blue glow has higher Blue than Red/Green (B > R + 30).
    
    whiteData = []
    for item in img_transparent.getdata():
        if item[3] == 0:
            # Already transparent background
            whiteData.append(item)
        else:
            r, g, b, a = item
            # If it's a dark pixel (text or dark metal)
            if r < 120 and g < 120 and b < 120:
                # Convert black/dark parts to clean white
                whiteData.append((255, 255, 255, a))
            # Or if it's the blue glow, we can keep it as is, or make it slightly brighter
            elif b > r + 30:
                # Keep blue glow
                whiteData.append((r, g, b, a))
            else:
                # Make other parts lighter to look elegant on dark backgrounds
                # Let's blend it towards white
                factor = 0.8
                nr = int(r + (255 - r) * factor)
                ng = int(g + (255 - g) * factor)
                nb = int(b + (255 - b) * factor)
                whiteData.append((nr, ng, nb, a))
                
    img_white = Image.new('RGBA', img.size)
    img_white.putdata(whiteData)
    
    # Save dark theme versions
    img_white.save(output_white, 'PNG')
    img_white.save(output_wave_white, 'PNG')
    print(f"Saved dark theme logo to {output_white} and {output_wave_white}")

if __name__ == '__main__':
    process_logos()

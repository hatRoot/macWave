import re
import base64
from PIL import Image
from io import BytesIO

logo_const_path = '/Users/joelduran/Documents/GitHub/MacWaveT2/logo_const.js'
with open(logo_const_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract LOGO_0_BASE64 data
m0 = re.search(r"LOGO_0_BASE64 = \{ data: 'data:image/png;base64,([^']+)'", content)
if m0:
    data_b64 = m0.group(1)
    img_data = base64.b64decode(data_b64)
    img = Image.open(BytesIO(img_data))
    print(f"Decoded LOGO_0_BASE64: size={img.size}, format={img.format}")
else:
    print("Could not find LOGO_0_BASE64 in logo_const.js")

# Extract LOGO_10_BASE64 data
m10 = re.search(r"LOGO_10_BASE64 = \{ data: 'data:image/png;base64,([^']+)'", content)
if m10:
    data_b64 = m10.group(1)
    img_data = base64.b64decode(data_b64)
    img = Image.open(BytesIO(img_data))
    print(f"Decoded LOGO_10_BASE64: size={img.size}, format={img.format}")
else:
    print("Could not find LOGO_10_BASE64 in logo_const.js")

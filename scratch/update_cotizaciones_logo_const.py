import re
import base64

# Update the cotizaciones/logo_const.js with the same new logo images
negro_path = '/Users/joelduran/Documents/GitHub/MacWaveT2/images/negro.png'
white_path = '/Users/joelduran/Documents/GitHub/MacWaveT2/images/logo_dashboard_white.png'
logo_const_path = '/Users/joelduran/Documents/GitHub/MacWaveT2/cotizaciones/logo_const.js'

with open(negro_path, 'rb') as f:
    negro_b64 = base64.b64encode(f.read()).decode('utf-8')
with open(white_path, 'rb') as f:
    white_b64 = base64.b64encode(f.read()).decode('utf-8')

with open(logo_const_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_logo_0 = f"const LOGO_0_BASE64 = {{ data: 'data:image/png;base64,{negro_b64}', w: 1024, h: 682 }};"
new_logo_10 = f"const LOGO_10_BASE64 = {{ data: 'data:image/png;base64,{white_b64}', w: 1024, h: 682 }};"

content = re.sub(
    r'const LOGO_0_BASE64\s*=\s*\{\s*data:\s*\'[^\']+\'\s*,\s*w:\s*\d+\s*,\s*h:\s*\d+\s*\};',
    new_logo_0,
    content
)
content = re.sub(
    r'const LOGO_10_BASE64\s*=\s*\{\s*data:\s*\'[^\']+\'\s*,\s*w:\s*\d+\s*,\s*h:\s*\d+\s*\};',
    new_logo_10,
    content
)

with open(logo_const_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("cotizaciones/logo_const.js updated!")

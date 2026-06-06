import re
import base64

def update_logo_const():
    logo_const_path = '/Users/joelduran/Documents/GitHub/MacWaveT2/logo_const.js'
    negro_path = '/Users/joelduran/Documents/GitHub/MacWaveT2/images/negro.png'
    white_path = '/Users/joelduran/Documents/GitHub/MacWaveT2/images/logo_dashboard_white.png'
    
    # 1. Read files and convert to base64
    with open(negro_path, 'rb') as f:
        negro_b64 = base64.b64encode(f.read()).decode('utf-8')
    with open(white_path, 'rb') as f:
        white_b64 = base64.b64encode(f.read()).decode('utf-8')
        
    # 2. Read logo_const.js
    with open(logo_const_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 3. Use regex to replace LOGO_0_BASE64 and LOGO_10_BASE64
    # The format is: const LOGO_0_BASE64 = { data: '...', w: ..., h: ... };
    
    new_logo_0 = f"const LOGO_0_BASE64 = {{ data: 'data:image/png;base64,{negro_b64}', w: 1024, h: 682 }};"
    new_logo_10 = f"const LOGO_10_BASE64 = {{ data: 'data:image/png;base64,{white_b64}', w: 1024, h: 682 }};"
    
    # Replace LOGO_0_BASE64 line
    content = re.sub(
        r'const LOGO_0_BASE64\s*=\s*\{\s*data:\s*\'[^\']+\'\s*,\s*w:\s*\d+\s*,\s*h:\s*\d+\s*\};',
        new_logo_0,
        content
    )
    
    # Replace LOGO_10_BASE64 line
    content = re.sub(
        r'const LOGO_10_BASE64\s*=\s*\{\s*data:\s*\'[^\']+\'\s*,\s*w:\s*\d+\s*,\s*h:\s*\d+\s*\};',
        new_logo_10,
        content
    )
    
    # 4. Save logo_const.js
    with open(logo_const_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("logo_const.js updated successfully with new base64 logos!")

if __name__ == '__main__':
    update_logo_const()

import os
import glob

workspace = '/Users/joelduran/Documents/GitHub/MacWaveT2'
matches = glob.glob(os.path.join(workspace, '**', 'logo_const.js'), recursive=True)

print("Found logo_const.js files:")
for m in matches:
    print(f"  {m}: size={os.path.getsize(m)} bytes")

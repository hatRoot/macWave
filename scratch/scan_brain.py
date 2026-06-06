import os
import glob

brain_dir = '/Users/joelduran/.gemini/antigravity-ide/brain/46c324bb-c2f1-4bbb-83c2-7a1eaae959f2'
if os.path.exists(brain_dir):
    files = glob.glob(os.path.join(brain_dir, '**', '*'), recursive=True)
    print("Files in brain directory:")
    for f in files:
        if os.path.isfile(f):
            print(f"{f}: size={os.path.getsize(f)} bytes")
else:
    print(f"Directory {brain_dir} does not exist")

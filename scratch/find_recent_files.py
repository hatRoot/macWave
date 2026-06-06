import os
import glob

workspace = '/Users/joelduran/Documents/GitHub/MacWaveT2'
files = glob.glob(os.path.join(workspace, '**', '*'), recursive=True)

# Sort files by modification time
files_with_mtime = []
for f in files:
    if os.path.isfile(f):
        files_with_mtime.append((f, os.path.getmtime(f)))

files_with_mtime.sort(key=lambda x: x[1], reverse=True)

print("Recently modified/added files:")
for f, mtime in files_with_mtime[:15]:
    print(f"{os.path.relpath(f, workspace)}: {mtime}")

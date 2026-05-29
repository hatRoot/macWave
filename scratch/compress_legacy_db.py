import urllib.request
import json
import ssl
import base64
from io import BytesIO
from PIL import Image

_sbUrl = 'https://lifxtyhvgnxjjqgbzare.supabase.co'
_sbKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxpZnh0eWh2Z254ampxZ2J6YXJlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE3MzAzNTgsImV4cCI6MjA4NzMwNjM1OH0.YCOLJUZaw5LNAyDyNrzhlJJJeUltRadrnjC1oNUCgFI'

headers = {
    "apikey": _sbKey,
    "Authorization": f"Bearer {_sbKey}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def compress_base64_image(base64_str):
    if not isinstance(base64_str, str) or not base64_str.startswith('data:image/'):
        return base64_str, False

    try:
        # Extract metadata prefix and raw data
        prefix, encoded = base64_str.split(',', 1)
        image_data = base64.b64decode(encoded)
        
        # Open image using Pillow
        img = Image.open(BytesIO(image_data))
        
        # Convert to RGB mode (JPEG doesn't support alpha channel)
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            img = img.convert('RGB')
        elif img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Resize if dimension exceeds 900px
        max_dim = 900
        width, height = img.size
        if width > max_dim or height > max_dim:
            ratio = min(max_dim / width, max_dim / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
        # Save compressed to memory buffer as JPEG
        out_buf = BytesIO()
        img.save(out_buf, format='JPEG', quality=35)
        compressed_bytes = out_buf.getvalue()
        
        # Re-encode to Base64
        compressed_encoded = base64.b64encode(compressed_bytes).decode('utf-8')
        new_base64_str = f"data:image/jpeg;base64,{compressed_encoded}"
        
        # Only use compressed version if it is indeed smaller
        if len(new_base64_str) < len(base64_str):
            return new_base64_str, True
            
    except Exception as e:
        print(f"      [Compression Error]: {e}")
        
    return base64_str, False

def run_migration():
    context = ssl._create_unverified_context()
    
    # 1. Fetch all ODS
    url = f"{_sbUrl}/rest/v1/ordenes_servicio?select=id,folio,cliente,status,notas"
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, context=context) as response:
            html = response.read().decode('utf-8')
            all_ods = json.loads(html)
    except Exception as e:
        print("Error fetching ODS from database:", e)
        return
        
    print(f"Fetched {len(all_ods)} service orders. Starting audit and compression...")
    
    total_original_bytes = 0
    total_compressed_bytes = 0
    modified_count = 0
    
    for idx, ods in enumerate(all_ods):
        ods_id = ods['id']
        folio = ods['folio']
        cliente = ods['cliente']
        notas_str = ods.get('notas') or ''
        
        if not notas_str:
            continue
            
        try:
            historial = json.loads(notas_str)
        except Exception as e:
            # Not JSON or corrupt
            continue
            
        if not isinstance(historial, list):
            continue
            
        # Let's check if there are any base64 images to compress
        row_modified = False
        original_size = len(notas_str)
        total_original_bytes += original_size
        
        print(f"\n[{idx+1}/{len(all_ods)}] Auditing Folio: {folio} | Cliente: {cliente} | Length: {original_size} chars")
        
        for entry_idx, entry in enumerate(historial):
            # Check img field
            img_val = entry.get('img')
            if img_val and isinstance(img_val, str) and img_val.startswith('data:image/'):
                original_img_len = len(img_val)
                new_img, compressed = compress_base64_image(img_val)
                if compressed:
                    entry['img'] = new_img
                    row_modified = True
                    print(f"   - Compressed 'img' in event {entry_idx}: {original_img_len} chars -> {len(new_img)} chars (Saved {original_img_len - len(new_img)} chars)")
                    
            # Check photos array field
            photos_val = entry.get('photos')
            if isinstance(photos_val, list):
                for p_idx, p in enumerate(photos_val):
                    if p and isinstance(p, str) and p.startswith('data:image/'):
                        original_p_len = len(p)
                        new_p, compressed = compress_base64_image(p)
                        if compressed:
                            photos_val[p_idx] = new_p
                            row_modified = True
                            print(f"   - Compressed 'photos[{p_idx}]' in event {entry_idx}: {original_p_len} chars -> {len(new_p)} chars (Saved {original_p_len - len(new_p)} chars)")
                            
        if row_modified:
            # Serialize back
            new_notas_str = json.dumps(historial)
            new_size = len(new_notas_str)
            total_compressed_bytes += new_size
            modified_count += 1
            
            print(f"   >>> SAVING CHANGES: {original_size} chars -> {new_size} chars (Total Row Savings: {original_size - new_size} chars, {(original_size - new_size) / original_size * 100:.1f}% reduction)")
            
            # 2. Update the row in Supabase
            update_url = f"{_sbUrl}/rest/v1/ordenes_servicio?id=eq.{ods_id}"
            update_data = json.dumps({"notas": new_notas_str}).encode('utf-8')
            update_req = urllib.request.Request(update_url, data=update_data, headers=headers, method="PATCH")
            
            try:
                with urllib.request.urlopen(update_req, context=context) as response:
                    response.read()
                print("   >>> SUCCESS: Database row updated successfully!")
            except Exception as e:
                print(f"   >>> ERROR UPDATING DATABASE ROW: {e}")
        else:
            total_compressed_bytes += original_size
            
    print("\n=======================================================")
    print("MIGRATION COMPLETED SUCCESSFULLY!")
    print(f"Modified Rows: {modified_count}")
    print(f"Total Original Notes Size: {total_original_bytes / (1024*1024):.2f} MB")
    print(f"Total Optimized Notes Size: {total_compressed_bytes / (1024*1024):.2f} MB")
    if total_original_bytes > 0:
        saved_bytes = total_original_bytes - total_compressed_bytes
        print(f"Total Database Payload Saved: {saved_bytes / (1024*1024):.2f} MB ({saved_bytes / total_original_bytes * 100:.1f}% space saved!)")
    print("=======================================================")

if __name__ == "__main__":
    run_migration()

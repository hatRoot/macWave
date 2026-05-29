import urllib.request
import json
import ssl

_sbUrl = 'https://lifxtyhvgnxjjqgbzare.supabase.co'
_sbKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxpZnh0eWh2Z254ampxZ2J6YXJlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE3MzAzNTgsImV4cCI6MjA4NzMwNjM1OH0.YCOLJUZaw5LNAyDyNrzhlJJJeUltRadrnjC1oNUCgFI'

headers = {
    "apikey": _sbKey,
    "Authorization": f"Bearer {_sbKey}"
}

url = f"{_sbUrl}/rest/v1/ordenes_servicio?select=id,folio,cliente,status,notas&limit=100"

req = urllib.request.Request(url, headers=headers)
context = ssl._create_unverified_context()

try:
    with urllib.request.urlopen(req, context=context) as response:
        html = response.read().decode('utf-8')
        data = json.loads(html)
except Exception as e:
    print(f"Error fetching: {e}")
    exit(1)

# Filter for recent or specific ODS
print(f"Total ODS fetched: {len(data)}")
target_folios = ['MW-20260321-9480', 'MW-20260321-9479', 'MW-20260326-9484', 'MW-20260311-9473']
for ods in data:
    if ods['folio'] in target_folios or 'Veronica' in ods.get('cliente', '') or 'David' in ods.get('cliente', ''):
        notes_str = ods.get('notas') or '[]'
        try:
            notes = json.loads(notes_str)
        except Exception as e:
            notes = []
        
        has_photos = False
        has_img = False
        photo_lens = []
        img_len = 0
        for n in notes:
            if n.get('photos'):
                has_photos = True
                photo_lens.append(len(n.get('photos')))
            if n.get('img'):
                has_img = True
                img_len = len(n.get('img'))
                
        print(f"\n=========================================")
        print(f"Folio: {ods['folio']} | Cliente: {ods['cliente']} | Status: {ods['status']}")
        print(f"Notes count: {len(notes)} | Has img: {has_img} | Has photos: {has_photos} (lens: {photo_lens})")
        if notes:
            for i, n in enumerate(notes[-3:]):
                note_idx = len(notes) - 3 + i if len(notes) >= 3 else i
                p_val = n.get('photos')
                p_info = f"Array of {len(p_val)} elements" if isinstance(p_val, list) else str(type(p_val))
                print(f"   [{note_idx}] Date: {n.get('date')} | Status: {n.get('status')} | text: {repr(n.get('text'))[:60]} | img present: {bool(n.get('img'))} | photos present: {bool(p_val)} ({p_info})")
                if p_val and isinstance(p_val, list) and len(p_val) > 0:
                    print(f"       First photo sample: {repr(p_val[0])[:120]}...")

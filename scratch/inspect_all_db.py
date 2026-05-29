import urllib.request
import json
import ssl

_sbUrl = 'https://lifxtyhvgnxjjqgbzare.supabase.co'
_sbKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxpZnh0eWh2Z254ampxZ2J6YXJlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE3MzAzNTgsImV4cCI6MjA4NzMwNjM1OH0.YCOLJUZaw5LNAyDyNrzhlJJJeUltRadrnjC1oNUCgFI'

headers = {
    "apikey": _sbKey,
    "Authorization": f"Bearer {_sbKey}"
}

# Fetch all ODS
url = f"{_sbUrl}/rest/v1/ordenes_servicio?select=id,folio,cliente,status,notas"

req = urllib.request.Request(url, headers=headers)
context = ssl._create_unverified_context()

try:
    with urllib.request.urlopen(req, context=context) as response:
        html = response.read().decode('utf-8')
        data = json.loads(html)
except Exception as e:
    print(f"Error fetching: {e}")
    exit(1)

print(f"Total ODS: {len(data)}")
for ods in data:
    notes_str = ods.get('notas') or '[]'
    try:
        notes = json.loads(notes_str)
    except Exception as e:
        notes = []
    
    for idx, n in enumerate(notes):
        p_val = n.get('photos')
        img_val = n.get('img')
        if p_val or img_val:
            print(f"Folio: {ods['folio']} | Cliente: {ods['cliente']} | Event index: {idx}")
            if img_val:
                print(f"   Legacy img present: {len(img_val)} chars, starts with {img_val[:50]}...")
            if p_val:
                print(f"   photos array present: {len(p_val)} items")
                for p_idx, p in enumerate(p_val):
                    print(f"      Photo {p_idx}: {len(p) if p else 0} chars, starts with {p[:50] if p else 'None'}...")

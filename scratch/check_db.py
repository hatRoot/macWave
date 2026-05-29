import urllib.request
import json

url = "https://lifxtyhvgnxjjqgbzare.supabase.co/rest/v1/ordenes_servicio?select=*"
headers = {
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxpZnh0eWh2Z254ampxZ2J6YXJlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE3MzAzNTgsImV4cCI6MjA4NzMwNjM1OH0.YCOLJUZaw5LNAyDyNrzhlJJJeUltRadrnjC1oNUCgFI",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxpZnh0eWh2Z254ampxZ2J6YXJlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE3MzAzNTgsImV4cCI6MjA4NzMwNjM1OH0.YCOLJUZaw5LNAyDyNrzhlJJJeUltRadrnjC1oNUCgFI"
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        html = response.read()
        data = json.loads(html.decode('utf-8'))
        
        # Sort in Python by updated_at or created_at desc
        data_sorted = sorted(data, key=lambda x: x.get('updated_at', '') or '', reverse=True)
        
        found = False
        for ods in data_sorted:
            notas = ods.get('notas')
            if notas:
                try:
                    hist = json.loads(notas)
                    has_photos = False
                    for entry in hist:
                        if entry.get('photos') and len(entry.get('photos')) > 0:
                            has_photos = True
                            break
                    if has_photos:
                        found = True
                        print("=========================================")
                        print(f"FOUND ODS WITH PHOTOS: {ods.get('folio')}")
                        print(f"ID: {ods.get('id')}")
                        print(f"Cliente: {ods.get('cliente')}")
                        print(f"Status: {ods.get('status')}")
                        print(f"Updated At: {ods.get('updated_at')}")
                        for idx, entry in enumerate(hist):
                            print(f"  Entry {idx + 1}:")
                            print(f"    Date: {entry.get('date')}")
                            print(f"    Status: {entry.get('status')}")
                            print(f"    Text: {entry.get('text')}")
                            photos = entry.get('photos')
                            if photos:
                                print(f"    Photos array: {len(photos)} items")
                                for p_idx, p in enumerate(photos):
                                    print(f"      ph[{p_idx}]: {p[:100]}... (len: {len(p)})")
                except Exception as e:
                    pass
        if not found:
            print("No ODS entries with photos array found.")
except Exception as e:
    print("Request failed:", e)

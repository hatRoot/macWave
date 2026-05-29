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
        
        found = False
        for ods in data:
            notas = ods.get('notas', '')
            if notas and 'base64' in notas:
                found = True
                print("=========================================")
                print(f"Folio: {ods.get('folio')}")
                print(f"ID: {ods.get('id')}")
                print(f"Cliente: {ods.get('cliente')}")
                print(f"Status: {ods.get('status')}")
                print(f"Notas Length: {len(str(notas))}")
                try:
                    hist = json.loads(notas)
                    print(f"JSON entries: {len(hist)}")
                    for idx, h in enumerate(hist):
                        img_present = 'img' in h and h['img'] is not None
                        photos_present = 'photos' in h and h['photos'] is not None
                        print(f"  Entry {idx + 1}: Date={h.get('date')}, Status={h.get('status')}, img={img_present}, photos={photos_present}")
                except Exception as e:
                    print(f"JSON parsing error: {e}")
        if not found:
            print("No rows containing base64 in 'notas' found.")
except Exception as e:
    print("Failed:", e)

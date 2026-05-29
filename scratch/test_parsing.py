import urllib.request
import json

url = "https://lifxtyhvgnxjjqgbzare.supabase.co/rest/v1/ordenes_servicio?id=eq.82b0e364-e427-4740-896b-bf0fca046070"
headers = {
    "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxpZnh0eWh2Z254ampxZ2J6YXJlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE3MzAzNTgsImV4cCI6MjA4NzMwNjM1OH0.YCOLJUZaw5LNAyDyNrzhlJJJeUltRadrnjC1oNUCgFI",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxpZnh0eWh2Z254ampxZ2J6YXJlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE3MzAzNTgsImV4cCI6MjA4NzMwNjM1OH0.YCOLJUZaw5LNAyDyNrzhlJJJeUltRadrnjC1oNUCgFI"
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        if data:
            ods = data[0]
            print("Folio:", ods.get('folio'))
            print("Notas Length:", len(ods.get('notas', '')))
            historial = json.loads(ods.get('notas', '[]'))
            for idx, ev in enumerate(historial):
                print(f"Entry {idx+1}: status={ev.get('status')}, date={ev.get('date')}, text={ev.get('text')}")
                print(f"  img type={type(ev.get('img'))}, img value starts with={str(ev.get('img'))[:50] if ev.get('img') else 'None'}")
                print(f"  photos type={type(ev.get('photos'))}, photos={ev.get('photos')}")
except Exception as e:
    print("Error:", e)

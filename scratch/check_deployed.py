import urllib.request
import ssl

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
req = urllib.request.Request("https://macwave.com.mx/status-ods", headers=headers)
context = ssl._create_unverified_context()
try:
    with urllib.request.urlopen(req, context=context) as response:
        content = response.read().decode('utf-8')
    print("Content Length:", len(content))
    print("Contains lightbox-modal:", "lightbox-modal" in content)
    print("Contains openLightbox:", "openLightbox" in content)
    print("Contains Para tu dispositivo Apple:", "Para tu dispositivo Apple" in content)
except Exception as e:
    print("Error:", e)

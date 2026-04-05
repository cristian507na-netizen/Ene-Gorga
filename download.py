import urllib.request
import re
import os

urls = {
    "cedi": "https://gruporey.com.pa/cedi/",
    "buenaventura": "https://buenaventura.com.pa/real-estate/peninsula-sur/",
    "thewoods": "https://thewoodssantamaria.com/",
    "caf": "https://mallolarquitectos.com/work/caf-northern-region-headquarters/",
    "mrprecio": "https://gruporey.com.pa/mr-precio/",
    "templo_puebla": "https://es.thechurchnews.com/templos/2024/03/26/templo-puebla-mexico-dia-de-medios-de-comunicacion-casa-abierta-fotos/",
    "templo_chile": "https://www.churchofjesuschrist.org/temples/details/antofagasta-chile-temple?lang=spa"
}

os.makedirs('assets/img', exist_ok=True)

for name, url in urls.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
        
        # try og:image
        match = re.search(r'<meta property="og:image" content="(.*?)"', html)
        img_url = match.group(1) if match else None
        
        if not img_url:
            # fallback to first large jpg/png
            imgs = re.findall(r'<img[^>]+src="([^">]+\.(?:jpg|png|webp))"', html)
            imgs = [img for img in imgs if 'logo' not in img.lower() and 'icon' not in img.lower()]
            if imgs:
                img_url = imgs[0]
                if img_url.startswith('/'):
                    from urllib.parse import urlparse
                    parsed = urlparse(url)
                    img_url = f"{parsed.scheme}://{parsed.netloc}{img_url}"

        if img_url:
            print(f"Downloading {name} from {img_url}")
            req_img = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            img_data = urllib.request.urlopen(req_img, timeout=10).read()
            ext = img_url.split('.')[-1].split('?')[0]
            if len(ext) > 4: ext = "jpg"
            with open(f"assets/img/{name}.{ext}", 'wb') as f:
                f.write(img_data)
        else:
            print(f"No image found for {name}")
    except Exception as e:
        print(f"Error for {name}: {e}")

import urllib.request
import re

urls = [
    "https://gruporey.com.pa/cedi/",
    "https://buenaventura.com.pa/real-estate/peninsula-sur/",
    "https://thewoodssantamaria.com/",
    "https://mallolarquitectos.com/work/caf-northern-region-headquarters/",
    "https://gruporey.com.pa/mr-precio/",
    "https://gruporey.com.pa/zaz/",
    "https://gruporey.com.pa/farma-ahorro/",
    "https://es.thechurchnews.com/templos/2024/03/26/templo-puebla-mexico-dia-de-medios-de-comunicacion-casa-abierta-fotos/",
    "https://www.churchofjesuschrist.org/temples/details/antofagasta-chile-temple?lang=spa"
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        images = re.findall(r'<img[^>]+src="([^">]+)"', html)
        og_image = re.findall(r'<meta property="og:image" content="([^">]+)"', html)
        if og_image:
            print(f"{url} -> OG: {og_image[0]}")
        else:
            images = [img for img in images if 'logo' not in img.lower() and ('jpg' in img.lower() or 'png' in img.lower())]
            if images:
                print(f"{url} -> IMG: {images[0]}")
    except Exception as e:
        print(f"Failed for {url}: {e}")

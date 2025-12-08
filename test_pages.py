import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_site.settings')
django.setup()

from django.test import Client
from django.urls import reverse

print("\n=== TEST EN DIRECT DES PAGES ===\n")

client = Client()

# Test pour yama-sakho
urls = [
    ('/profil/nom=yama-sakho&profession=data-analyst/projets/', 'Projets'),
    ('/profil/nom=yama-sakho&profession=data-analyst/services/', 'Services'),
    ('/profil/nom=yama-sakho&profession=data-analyst/blog/', 'Blog'),
]

for url, page_name in urls:
    print(f"\n📄 Page {page_name}: {url}")
    try:
        response = client.get(url)
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Chercher le titre dans le HTML
            import re
            # Chercher le H1 avec class="section-title"
            match = re.search(r'<h1[^>]*class="section-title"[^>]*>(.*?)</h1>', content, re.DOTALL)
            if match:
                title_html = match.group(1)
                # Enlever les balises HTML
                title_text = re.sub(r'<[^>]+>', '', title_html).strip()
                print(f"  ✅ Titre trouvé: '{title_text}'")
            else:
                print(f"  ❌ Titre non trouvé dans le HTML")
                # Chercher si le code Django brut apparaît
                if '{{ site_profile' in content:
                    print(f"  ⚠️  Code Django brut détecté dans le HTML!")
        else:
            print(f"  ❌ Erreur {response.status_code}")
    except Exception as e:
        print(f"  ❌ Exception: {e}")

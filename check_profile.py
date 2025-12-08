import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_site.settings')
django.setup()

from app_acceuil.models import SiteProfile

# Chercher le profil yama-sakho
profiles = SiteProfile.objects.all()
print(f"\n=== TOUS LES PROFILS ===")
for p in profiles:
    print(f"\nSlug: {p.slug}")
    print(f"  - services_page_title: '{p.services_page_title}'")
    print(f"  - blog_page_title: '{p.blog_page_title}'")
    print(f"  - projects_page_title: '{p.projects_page_title}'")
    print(f"  - is_default: {p.is_default}")
    print(f"  - is_published: {p.is_published}")

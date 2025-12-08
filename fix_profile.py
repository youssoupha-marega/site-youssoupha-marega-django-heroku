import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_site.settings')
django.setup()

from app_acceuil.models import SiteProfile

# Mettre à jour le profil yama-sakho
profile = SiteProfile.objects.get(slug='yama-sakho-data-analyst')
profile.services_page_title = 'Services offerts YAMA'
profile.blog_page_title = 'Blog YAMA'
profile.save()

print("✅ Profil mis à jour!")
print(f"  - services_page_title: '{profile.services_page_title}'")
print(f"  - blog_page_title: '{profile.blog_page_title}'")

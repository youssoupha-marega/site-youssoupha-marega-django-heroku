import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_site.settings')
django.setup()

from app_acceuil.models import SiteProfile

print("\n=== DIAGNOSTIC COMPLET ===\n")

# Vérifier tous les profils
profiles = SiteProfile.objects.all()
for p in profiles:
    print(f"PROFIL: {p.first_name} {p.last_name}")
    print(f"  Slug: {p.slug}")
    print(f"  is_default: {p.is_default}")
    print(f"  is_published: {p.is_published}")
    print(f"\nTITRES DES PAGES:")
    print(f"  - projects_page_title: '{p.projects_page_title}'")
    print(f"  - services_page_title: '{p.services_page_title}'")
    print(f"  - blog_page_title: '{p.blog_page_title}'")
    print(f"\nLABELS NAVBAR:")
    print(f"  - projects_navbar_label: '{p.projects_navbar_label}'")
    print(f"  - services_navbar_label: '{p.services_navbar_label}'")
    print(f"  - blog_navbar_label: '{p.blog_navbar_label}'")
    print("\n" + "="*60 + "\n")

# Tester la récupération du profil comme le fait la vue
from django.test import RequestFactory
from app_acceuil.base_views import ProfileBasedListView

print("\n=== TEST RÉCUPÉRATION PROFIL PAR VUE ===\n")

class TestView(ProfileBasedListView):
    model = SiteProfile

factory = RequestFactory()
request = factory.get('/profil/nom=yama-sakho&profession=data-analyst/services/')
request.resolver_match = type('obj', (object,), {'kwargs': {'nom': 'yama-sakho', 'profession': 'data-analyst'}})()

view = TestView()
view.request = request
view.kwargs = {'nom': 'yama-sakho', 'profession': 'data-analyst'}

try:
    profile = view.get_profile()
    print(f"Profil récupéré par la vue: {profile.slug}")
    print(f"  - services_page_title: '{profile.services_page_title}'")
    print(f"  - blog_page_title: '{profile.blog_page_title}'")
    print(f"  - projects_page_title: '{profile.projects_page_title}'")
except Exception as e:
    print(f"ERREUR: {e}")

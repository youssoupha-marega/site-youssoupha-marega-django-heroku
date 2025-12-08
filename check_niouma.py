import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_site.settings')
django.setup()

from app_acceuil.models import SiteProfile

print("\n=== VÉRIFICATION PROFIL NIOUMA TOURE ===\n")

# Chercher le profil Niouma
profiles = SiteProfile.objects.filter(first_name__icontains='niouma')
if not profiles.exists():
    profiles = SiteProfile.objects.filter(last_name__icontains='toure')

if profiles.exists():
    for p in profiles:
        print(f"✅ Profil trouvé: {p.first_name} {p.last_name}")
        print(f"  Slug: {p.slug}")
        print(f"  is_published: {p.is_published}")
        print(f"  is_default: {p.is_default}")
        print(f"\nTITRES:")
        print(f"  - projects_page_title: '{p.projects_page_title}'")
        print(f"  - services_page_title: '{p.services_page_title}'")
        print(f"  - blog_page_title: '{p.blog_page_title}'")
        
        # Vérifier s'il y a du code Django brut
        if '{{' in p.services_page_title or '{%' in p.services_page_title:
            print(f"\n⚠️  PROBLÈME: Le champ services_page_title contient du code Django!")
            print(f"  Correction en cours...")
            p.services_page_title = f"Services {p.first_name}"
            p.save()
            print(f"  ✅ Corrigé: '{p.services_page_title}'")
            
        if '{{' in p.blog_page_title or '{%' in p.blog_page_title:
            print(f"\n⚠️  PROBLÈME: Le champ blog_page_title contient du code Django!")
            print(f"  Correction en cours...")
            p.blog_page_title = f"Blog {p.first_name}"
            p.save()
            print(f"  ✅ Corrigé: '{p.blog_page_title}'")
else:
    print("❌ Aucun profil trouvé pour Niouma Toure")
    print("\nTous les profils:")
    for p in SiteProfile.objects.all():
        print(f"  - {p.first_name} {p.last_name} (slug: {p.slug})")

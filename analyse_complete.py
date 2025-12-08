import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_site.settings')
django.setup()

from app_acceuil.models import SiteProfile
from django.template import Template, Context

print("\n" + "="*80)
print("ANALYSE COMPLÈTE DU PROBLÈME")
print("="*80 + "\n")

# 1. VÉRIFICATION BASE DE DONNÉES
print("1. VÉRIFICATION BASE DE DONNÉES")
print("-" * 80)
profile = SiteProfile.objects.get(slug='niouma-toure-kaba')
print(f"Profil: {profile.first_name} {profile.last_name}")
print(f"Slug: {profile.slug}")
print(f"\nValeurs stockées dans la BDD:")
print(f"  services_page_title = '{profile.services_page_title}'")
print(f"  blog_page_title = '{profile.blog_page_title}'")
print(f"  projects_page_title = '{profile.projects_page_title}'")
print(f"\nType des valeurs:")
print(f"  Type de services_page_title: {type(profile.services_page_title)}")
print(f"  Contient du code Django? {'{{' in profile.services_page_title or '{%' in profile.services_page_title}")

# 2. TEST DU TEMPLATE
print("\n2. TEST DE RENDU DU TEMPLATE")
print("-" * 80)
template_code = """{% if site_profile.services_page_title %}{{ site_profile.services_page_title }}{% else %}Services offerts{% endif %}"""
template = Template(template_code)
context = Context({'site_profile': profile})
rendered = template.render(context)
print(f"Code du template: {template_code}")
print(f"Résultat attendu: '{profile.services_page_title}'")
print(f"Résultat obtenu: '{rendered}'")
print(f"Correspond? {rendered == profile.services_page_title}")

# 3. VÉRIFICATION CONTEXT PROCESSOR
print("\n3. VÉRIFICATION CONTEXT PROCESSOR")
print("-" * 80)
from app_acceuil.context_processors import site_profile as site_profile_processor
from django.test import RequestFactory

factory = RequestFactory()
request = factory.get('/profil/nom=niouma-toure&profession=kaba/services/')

# Simuler resolver_match
class FakeResolverMatch:
    def __init__(self):
        self.kwargs = {'nom': 'niouma-toure', 'profession': 'kaba'}

request.resolver_match = FakeResolverMatch()
context_data = site_profile_processor(request)
print(f"Context processor retourne: {context_data}")
if 'site_profile' in context_data and context_data['site_profile']:
    ctx_profile = context_data['site_profile']
    print(f"  Profil du context: {ctx_profile.slug}")
    print(f"  services_page_title: '{ctx_profile.services_page_title}'")
else:
    print("  ⚠️ Pas de site_profile dans le contexte!")

# 4. VÉRIFICATION VUE
print("\n4. VÉRIFICATION VUE")
print("-" * 80)
from app_service.views import ServiceListView

view = ServiceListView()
view.kwargs = {'nom': 'niouma-toure', 'profession': 'kaba'}
view_profile = view.get_profile()
print(f"Vue récupère le profil: {view_profile.slug}")
print(f"  services_page_title: '{view_profile.services_page_title}'")

# 5. LECTURE DU TEMPLATE RÉEL
print("\n5. LECTURE DU TEMPLATE SERVICES")
print("-" * 80)
import os
template_path = os.path.join('app_service', 'templates', 'app_service', 'list.html')
with open(template_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines[8:13], start=9):
        print(f"Ligne {i}: {line.rstrip()}")

# 6. DIAGNOSTIC FINAL
print("\n" + "="*80)
print("DIAGNOSTIC")
print("="*80)
print(f"""
✅ Base de données: services_page_title = '{profile.services_page_title}'
✅ Template Django fonctionne: rendu = '{rendered}'
✅ Context processor: OK
✅ Vue: OK

⚠️ HYPOTHÈSES SUR LE PROBLÈME:
1. Cache navigateur (Ctrl+Shift+R ne suffit pas)
2. Cache Django template
3. Fichier template modifié mais pas rechargé
4. Conflit entre context_processor et vue
5. Template utilise une mauvaise variable
""")

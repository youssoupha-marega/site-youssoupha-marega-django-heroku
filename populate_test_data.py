"""
Script pour créer un superuser et générer du contenu de test.

Usage: python manage.py shell < populate_test_data.py
"""

from django.contrib.auth.models import User
from app_acceuil.models import SiteProfile, Section, SectionItem
from app_projet.models import Project
from app_blog.models import BlogPost
from app_service.models import Service

# Créer superuser si nécessaire
if not User.objects.filter(username='ymarega').exists():
    User.objects.create_superuser(
        username='ymarega',
        email='youssouphamarega@gmail.com',
        password='B13nvenue869'
    )
    print("✅ Superuser créé: ymarega")
else:
    print("ℹ️  Superuser existe déjà")

# Créer profil par défaut
profile, created = SiteProfile.objects.get_or_create(
    first_name="Youssoupha",
    last_name="Marega",
    defaults={
        'profession': "Data Scientist",
        'email': "youssouphamarega@gmail.com",
        'location': "Montréal, Canada",
        'bio': "<p>Passionné par la science des données et le développement web.</p>",
        'is_published': True,
        'is_default': True,
        'linkedin_url': "https://linkedin.com/in/youssouphamarega",
        'github_url': "https://github.com/youssoupha-marega",
    }
)
print(f"{'✅ Profil créé' if created else 'ℹ️  Profil existe'}: {profile}")

# Créer sections
competences, _ = Section.objects.get_or_create(
    profile=profile,
    title="Compétences Techniques",
    section_type="competences",
    defaults={'is_active': True, 'order': 1}
)

items_competences = [
    ("Python", "Expert", 1),
    ("Django", "Avancé", 2),
    ("React", "Intermédiaire", 3),
    ("PostgreSQL", "Avancé", 4),
]

for title, subtitle, order in items_competences:
    SectionItem.objects.get_or_create(
        section=competences,
        title=title,
        defaults={'subtitle': subtitle, 'order': order}
    )

print(f"✅ Section Compétences créée avec {len(items_competences)} items")

# Créer section Formation
formation, _ = Section.objects.get_or_create(
    profile=profile,
    title="Formation",
    section_type="formation",
    defaults={'is_active': True, 'order': 2}
)

SectionItem.objects.get_or_create(
    section=formation,
    title="Master en Science des Données",
    defaults={
        'subtitle': "Université de Montréal",
        'date': "2020-2022",
        'order': 1
    }
)

print("✅ Section Formation créée")

# Créer des projets avec la nouvelle architecture
projets_data = [
    {
        'title': "Portfolio Django avec Multi-Profils",
        'resume': "Application Django permettant de gérer plusieurs profils de portfolio avec système de sections dynamiques.",
        'content': "<h2>Description</h2><p>Ce projet utilise Django 5.1 et implémente une architecture modulaire avec héritage de modèles abstraits.</p><h3>Technologies</h3><ul><li>Django 5.1.6</li><li>Python 3.12</li><li>PostgreSQL</li></ul>",
        'featured': True,
        'github_url': "https://github.com/youssoupha-marega/portfolio-django",
    },
    {
        'title': "API REST avec Django REST Framework",
        'resume': "API complète pour gérer des données de machine learning avec authentification JWT.",
        'content': "<h2>Fonctionnalités</h2><p>API REST sécurisée avec DRF, JWT, et documentation Swagger.</p>",
        'featured': True,
        'demo_url': "https://api-demo.youssouphamarega.com",
    },
    {
        'title': "Dashboard d'Analyse de Données",
        'resume': "Application web interactive pour visualiser et analyser des données avec Plotly et Dash.",
        'content': "<h2>Technologies</h2><p>Python, Plotly, Dash, Pandas, NumPy</p>",
        'featured': False,
    }
]

for data in projets_data:
    project, created = Project.objects.get_or_create(
        title=data['title'],
        defaults=data
    )
    if created:
        profile.published_projects.add(project)
        if data.get('featured'):
            profile.featured_projects.add(project)

print(f"✅ {len(projets_data)} projets créés")

# Créer des articles de blog
articles_data = [
    {
        'title': "Refactoring Django : L'approche hybride avec modèles abstraits",
        'resume': "Comment réduire 40% de code dupliqué avec l'héritage de modèles abstraits.",
        'content': "<h2>Introduction</h2><p>Dans cet article, nous explorons comment utiliser les modèles abstraits Django pour créer une architecture DRY.</p><h2>Avantages</h2><ul><li>Réduction du code</li><li>Meilleure maintenabilité</li><li>Tests partagés</li></ul>",
        'featured': True,
        'tags': "django, python, refactoring, architecture",
        'read_time': 8,
    },
    {
        'title': "Guide complet de Django Class-Based Views",
        'resume': "Maîtrisez les CBV Django pour des vues réutilisables et élégantes.",
        'content': "<h2>Pourquoi les CBV ?</h2><p>Les Class-Based Views offrent une meilleure réutilisation du code.</p>",
        'featured': True,
        'tags': "django, cbv, python",
        'read_time': 12,
    },
]

for data in articles_data:
    article, created = BlogPost.objects.get_or_create(
        title=data['title'],
        defaults=data
    )
    if created:
        profile.published_articles.add(article)
        if data.get('featured'):
            profile.featured_articles.add(article)

print(f"✅ {len(articles_data)} articles créés")

# Créer des services
services_data = [
    {
        'title': "Développement d'Applications Django",
        'resume': "Création d'applications web sur mesure avec Django et Python.",
        'content': "Je développe des applications web robustes et scalables avec Django, de la conception à la mise en production.",
        'featured': True,
        'price': "150.00",
        'duration': "À partir de 2 semaines",
    },
    {
        'title': "Consultation en Science des Données",
        'resume': "Analyse de données et création de modèles prédictifs.",
        'content': "Services de consultation pour vos projets de data science : analyse exploratoire, modélisation prédictive, visualisation.",
        'featured': True,
        'price': "200.00",
        'duration': "Projet sur mesure",
        'calendly_url': "https://calendly.com/youssouphamarega",
    },
]

for data in services_data:
    service, created = Service.objects.get_or_create(
        title=data['title'],
        defaults=data
    )
    if created:
        profile.published_services.add(service)
        if data.get('featured'):
            profile.featured_services.add(service)

print(f"✅ {len(services_data)} services créés")

print("\n" + "="*60)
print("🎉 DONNÉES DE TEST CRÉÉES AVEC SUCCÈS !")
print("="*60)
print(f"\n📊 Résumé:")
print(f"   • Superuser: ymarega / B13nvenue869")
print(f"   • Profil: {profile.first_name} {profile.last_name}")
print(f"   • Projets: {Project.objects.count()}")
print(f"   • Articles: {BlogPost.objects.count()}")
print(f"   • Services: {Service.objects.count()}")
print(f"   • Sections: {Section.objects.count()}")
print(f"\n🌐 Accédez à:")
print(f"   • Site: http://127.0.0.1:8000/")
print(f"   • Admin: http://127.0.0.1:8000/admin/")
print(f"   • Login: ymarega / B13nvenue869")
print("\n✨ La nouvelle architecture hybride est prête à l'emploi !")

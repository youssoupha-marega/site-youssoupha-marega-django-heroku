"""
Test unitaire pour vérifier l'affichage des métadonnées de services dans l'accueil
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from app_acceuil.models import SiteProfile
from app_service.models import Service
from datetime import datetime

class ServiceMetadataTest(TestCase):
    def setUp(self):
        """Prépare les données de test"""
        # Créer un SiteProfile
        self.profile = SiteProfile.objects.create(
            first_name="Test",
            last_name="User",
            profession="Developer",
            email="test@example.com",
            is_default=True,
            is_published=True,
            # Activer les métadonnées pour Services - Accueil
            services_show_author_home=True,
            services_show_profession_home=True,
            services_show_publish_date_home=True,
            services_show_update_date_home=True
        )
        
        # Créer un service avec métadonnées
        self.service = Service.objects.create(
            title="Service Test",
            slug="service-test",
            resume="Résumé du service test",
            content="Contenu du service test",
            author_name="Youssoupha Marega",
            author_profession="Data Scientist",
            author_email="youssoupha@example.com",
            published_at=datetime(2025, 12, 6),
            updated_at=datetime(2025, 12, 8)
        )
        # Publier le service
        self.service.is_published = True
        self.service.save()
        
        # Ajouter le service au profil
        self.profile.published_services.add(self.service)
        self.profile.featured_services.add(self.service)
        
        self.client = Client()
    
    def test_service_has_metadata(self):
        """Vérifier que le service a bien des métadonnées"""
        print("\n=== TEST 1: Vérification des métadonnées du service ===")
        print(f"Service title: {self.service.title}")
        print(f"Author name: {self.service.author_name}")
        print(f"Author profession: {self.service.author_profession}")
        print(f"Published at: {self.service.published_at}")
        print(f"Updated at: {self.service.updated_at}")
        
        self.assertEqual(self.service.author_name, "Youssoupha Marega")
        self.assertEqual(self.service.author_profession, "Data Scientist")
        self.assertIsNotNone(self.service.published_at)
        self.assertIsNotNone(self.service.updated_at)
    
    def test_profile_metadata_settings(self):
        """Vérifier que les paramètres de métadonnées du profil sont actifs"""
        print("\n=== TEST 2: Vérification des paramètres du SiteProfile ===")
        print(f"services_show_author_home: {self.profile.services_show_author_home}")
        print(f"services_show_profession_home: {self.profile.services_show_profession_home}")
        print(f"services_show_publish_date_home: {self.profile.services_show_publish_date_home}")
        print(f"services_show_update_date_home: {self.profile.services_show_update_date_home}")
        
        self.assertTrue(self.profile.services_show_author_home)
        self.assertTrue(self.profile.services_show_profession_home)
        self.assertTrue(self.profile.services_show_publish_date_home)
        self.assertTrue(self.profile.services_show_update_date_home)
    
    def test_home_page_context(self):
        """Vérifier que la page d'accueil contient le service et le profil"""
        print("\n=== TEST 3: Vérification du contexte de la page d'accueil ===")
        response = self.client.get('/')
        
        print(f"Status code: {response.status_code}")
        print(f"site_profile in context: {'site_profile' in response.context}")
        print(f"services in context: {'services' in response.context}")
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('site_profile', response.context)
        self.assertIn('services', response.context)
        
        services = response.context['services']
        print(f"Nombre de services: {len(services)}")
        
        if services:
            service = services[0]
            print(f"Premier service: {service.title}")
            print(f"Author name: {service.author_name}")
            print(f"Author profession: {service.author_profession}")
    
    def test_home_page_renders_metadata(self):
        """Vérifier que les métadonnées sont rendues dans le HTML"""
        print("\n=== TEST 4: Vérification du rendu HTML des métadonnées ===")
        response = self.client.get('/')
        content = response.content.decode('utf-8')
        
        # Chercher les métadonnées dans le HTML
        has_author = "Youssoupha Marega" in content
        has_profession = "Data Scientist" in content
        has_date = "06 Dec 2025" in content or "6 Dec 2025" in content or "Dec" in content
        
        print(f"HTML contient 'Youssoupha Marega': {has_author}")
        print(f"HTML contient 'Data Scientist': {has_profession}")
        print(f"HTML contient une date: {has_date}")
        
        if not has_author:
            print("\n⚠️ PROBLÈME: L'auteur n'apparaît pas dans le HTML")
            print("Extrait du HTML autour de 'Service Test':")
            if "Service Test" in content:
                idx = content.find("Service Test")
                print(content[max(0, idx-500):min(len(content), idx+500)])
        
        self.assertTrue(has_author, "L'auteur devrait apparaître dans le HTML")

if __name__ == '__main__':
    import django
    import os
    import sys
    
    # Configuration Django
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_site.settings')
    django.setup()
    
    # Exécuter les tests
    from django.test.utils import get_runner
    from django.conf import settings
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2)
    failures = test_runner.run_tests(["__main__"])
    sys.exit(bool(failures))

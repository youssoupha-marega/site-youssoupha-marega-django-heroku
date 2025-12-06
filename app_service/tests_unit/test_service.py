"""
Tests pour l'application app_service.

Couvre:
- Modèle: Service
- Vues: service_list, service_detail, profile_service_list, profile_service_detail
- URLs: racine et profil
"""

from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from app_service.models import Service
from app_acceuil.models import SiteProfile


class ServiceModelTest(TestCase):
    """Tests pour le modèle Service."""
    
    def setUp(self):
        """Créer des services de test."""
        self.service = Service.objects.create(
            title="Analyse de données",
            resume="Service d'analyse de données professionnelle",
            content="Description complète du service d'analyse",
            author_name="Yama Sakho",
            author_email="yama@example.com",
            author_profession="Data Analyst",
            calendly_url="https://calendly.com/yama-sakho/consultation",
            price=Decimal("150.00"),
            duration="1 heure"
        )
    
    def test_service_creation(self):
        """Tester la création d'un service."""
        self.assertEqual(self.service.title, "Analyse de données")
        self.assertEqual(self.service.author_name, "Yama Sakho")
        self.assertEqual(self.service.calendly_url, "https://calendly.com/yama-sakho/consultation")
        self.assertEqual(self.service.price, Decimal("150.00"))
        self.assertEqual(self.service.duration, "1 heure")
    
    def test_service_slug_generation(self):
        """Tester la génération du slug."""
        self.assertEqual(self.service.slug, "analyse-de-donnees")
    
    def test_service_get_absolute_url(self):
        """Tester get_absolute_url."""
        url = self.service.get_absolute_url()
        expected = reverse('service_detail', kwargs={'slug': self.service.slug})
        self.assertEqual(url, expected)
    
    def test_service_str_method(self):
        """Tester la méthode __str__."""
        self.assertEqual(str(self.service), "Analyse de données")
    
    def test_service_optional_fields(self):
        """Tester les champs optionnels."""
        service = Service.objects.create(
            title="Minimal Service",
            resume="Resume",
            content="Content",
            author_name="Author",
            author_email="test@example.com",
            author_profession="Consultant"
        )
        self.assertEqual(service.calendly_url, "")
        self.assertIsNone(service.price)
        self.assertEqual(service.duration, "")


class ServiceListViewTest(TestCase):
    """Tests pour la vue de liste des services (racine)."""
    
    def setUp(self):
        """Créer des services de test."""
        self.client = Client()
        
        self.service1 = Service.objects.create(
            title="Service 1",
            resume="Resume 1",
            content="Content 1",
            author_name="Author",
            author_email="test@example.com",
            author_profession="Consultant"
        )
        
        self.service2 = Service.objects.create(
            title="Service 2",
            resume="Resume 2",
            content="Content 2",
            author_name="Author",
            author_email="test@example.com",
            author_profession="Consultant"
        )
    
    def test_list_view_status_code(self):
        """Tester que la page de liste se charge."""
        response = self.client.get(reverse('service_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_list_view_uses_correct_template(self):
        """Tester que la vue utilise le bon template."""
        response = self.client.get(reverse('service_list'))
        self.assertTemplateUsed(response, 'app_service/list.html')
    
    def test_list_view_contains_services(self):
        """Tester que la vue contient les services."""
        response = self.client.get(reverse('service_list'))
        self.assertIn('services', response.context)
        self.assertEqual(len(response.context['services']), 2)
    
    def test_list_view_services_ordered_by_date(self):
        """Tester que les services sont triés par date."""
        response = self.client.get(reverse('service_list'))
        services = list(response.context['services'])
        self.assertEqual(len(services), 2)
        self.assertGreaterEqual(services[0].created_at, services[1].created_at)


class ServiceDetailViewTest(TestCase):
    """Tests pour la vue de détail d'un service (racine)."""
    
    def setUp(self):
        """Créer un service de test."""
        self.client = Client()
        
        self.service = Service.objects.create(
            title="Test Service",
            resume="Test resume",
            content="Test content",
            author_name="Author",
            author_email="test@example.com",
            author_profession="Consultant"
        )
    
    def test_detail_view_status_code(self):
        """Tester que la page de détail se charge."""
        response = self.client.get(
            reverse('service_detail', kwargs={'slug': self.service.slug})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_detail_view_uses_correct_template(self):
        """Tester que la vue utilise le bon template."""
        response = self.client.get(
            reverse('service_detail', kwargs={'slug': self.service.slug})
        )
        self.assertTemplateUsed(response, 'app_service/detail.html')
    
    def test_detail_view_contains_service(self):
        """Tester que la vue contient le service."""
        response = self.client.get(
            reverse('service_detail', kwargs={'slug': self.service.slug})
        )
        self.assertEqual(response.context['service'].id, self.service.id)
    
    def test_detail_view_404_for_invalid_slug(self):
        """Tester que la vue retourne 404 pour un slug invalide."""
        response = self.client.get(
            reverse('service_detail', kwargs={'slug': 'slug-inexistant'})
        )
        self.assertEqual(response.status_code, 404)


class ProfileServiceViewsTest(TestCase):
    """Tests pour les vues de services avec contexte profil."""
    
    def setUp(self):
        """Créer un profil et des services de test."""
        self.client = Client()
        
        # Créer un profil
        self.profile = SiteProfile.objects.create(
            first_name="Yama",
            last_name="Sakho",
            profession="Data Analyst",
            is_published=True,
            is_default=False
        )
        
        # Créer des services
        self.service1 = Service.objects.create(
            title="Service 1",
            resume="Resume 1",
            content="Content 1",
            author_name="Yama Sakho",
            author_email="yama@example.com",
            author_profession="Data Analyst"
        )
        
        self.service2 = Service.objects.create(
            title="Service 2",
            resume="Resume 2",
            content="Content 2",
            author_name="Yama Sakho",
            author_email="yama@example.com",
            author_profession="Data Analyst"
        )
        
        # Associer les services au profil
        self.profile.published_services.add(self.service1, self.service2)
    
    def test_profile_list_view_status_code(self):
        """Tester que la liste profil se charge."""
        response = self.client.get(
            reverse('profile_service_list', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst'
            })
        )
        self.assertEqual(response.status_code, 200)
    
    def test_profile_list_view_contains_profile_services(self):
        """Tester que la liste contient les services du profil."""
        response = self.client.get(
            reverse('profile_service_list', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst'
            })
        )
        self.assertIn('services', response.context)
        self.assertEqual(len(response.context['services']), 2)
    
    def test_profile_list_view_contains_profile_context(self):
        """Tester que le contexte contient le profil."""
        response = self.client.get(
            reverse('profile_service_list', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst'
            })
        )
        self.assertIn('site_profile', response.context)
        self.assertEqual(response.context['site_profile'].id, self.profile.id)
    
    def test_profile_detail_view_status_code(self):
        """Tester que le détail profil se charge."""
        response = self.client.get(
            reverse('profile_service_detail', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst',
                'slug': self.service1.slug
            })
        )
        self.assertEqual(response.status_code, 200)
    
    def test_profile_detail_view_contains_service(self):
        """Tester que le détail contient le service."""
        response = self.client.get(
            reverse('profile_service_detail', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst',
                'slug': self.service1.slug
            })
        )
        self.assertEqual(response.context['service'].id, self.service1.id)
    
    def test_profile_detail_404_if_profile_not_found(self):
        """Tester 404 si le profil n'existe pas."""
        response = self.client.get(
            reverse('profile_service_detail', kwargs={
                'nom': 'invalid-name',
                'profession': 'invalid-profession',
                'slug': self.service1.slug
            })
        )
        self.assertEqual(response.status_code, 404)


class ServiceURLTest(TestCase):
    """Tests pour les URLs des services."""
    
    def test_root_list_url_resolves(self):
        """Tester que l'URL de liste racine est correcte."""
        url = reverse('service_list')
        self.assertEqual(url, '/services/')
    
    def test_root_detail_url_resolves(self):
        """Tester que l'URL de détail racine est correcte."""
        url = reverse('service_detail', kwargs={'slug': 'test-service'})
        self.assertEqual(url, '/services/test-service/')
    
    def test_profile_list_url_resolves(self):
        """Tester que l'URL de liste profil est correcte."""
        url = reverse('profile_service_list', kwargs={
            'nom': 'yama-sakho',
            'profession': 'data-analyst'
        })
        self.assertEqual(url, '/profil/nom=yama-sakho&profession=data-analyst/services/')
    
    def test_profile_detail_url_resolves(self):
        """Tester que l'URL de détail profil est correcte."""
        url = reverse('profile_service_detail', kwargs={
            'nom': 'yama-sakho',
            'profession': 'data-analyst',
            'slug': 'test-service'
        })
        self.assertEqual(
            url,
            '/profil/nom=yama-sakho&profession=data-analyst/services/test-service/'
        )


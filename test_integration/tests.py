"""
Tests d'intégration pour l'ensemble du site.

Pour exécuter: python manage.py test test_integration

Couvre:
- Navigation complète entre les pages
- Maintien du contexte profil dans les URLs
- Pool architecture (un contenu disponible pour plusieurs profils)
- Génération correcte des URLs avec slugs
- Flux utilisateur complets
"""

from django.test import TestCase, Client
from django.urls import reverse
from app_acceuil.models import SiteProfile
from app_projet.models import Project
from app_blog.models import BlogPost
from app_service.models import Service


class NavigationFlowTest(TestCase):
    """Tests de flux de navigation complet."""
    
    def setUp(self):
        """Créer un environnement de test."""
        self.client = Client()
        
        # Créer un profil
        self.profile = SiteProfile.objects.create(
            first_name="Yama",
            last_name="Sakho",
            profession="Data Analyst",
            is_published=True,
            is_default=False
        )
        
        # Créer du contenu
        self.project = Project.objects.create(
            title="Dashboard Analytics",
            resume="Dashboard interactif",
            content="<p>Contenu détaillé</p>",
            author_name="Yama Sakho",
            author_email="yama@example.com",
            author_profession="Data Analyst"
        )
        
        self.article = BlogPost.objects.create(
            title="Introduction ML",
            resume="Guide ML",
            content="<p>Contenu ML</p>",
            author_name="Yama Sakho",
            author_email="yama@example.com",
            author_profession="Data Analyst"
        )
        
        self.service = Service.objects.create(
            title="Consultation Data",
            resume="Service consultation",
            content="Description service",
            author_name="Yama Sakho",
            author_email="yama@example.com",
            author_profession="Data Analyst"
        )
        
        # Associer au profil
        self.profile.published_projects.add(self.project)
        self.profile.published_articles.add(self.article)
        self.profile.published_services.add(self.service)
    
    def test_profile_home_loads(self):
        """Tester que la page profil se charge."""
        response = self.client.get(
            reverse('profile_home', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst'
            })
        )
        self.assertEqual(response.status_code, 200)
    
    def test_profile_project_flow(self):
        """Tester le flux complet projets."""
        # Liste
        response = self.client.get(
            reverse('profile_projet_list', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst'
            })
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['projets']), 1)
        
        # Détail
        response = self.client.get(
            reverse('profile_projet_detail', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst',
                'slug': self.project.slug
            })
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['projet'].id, self.project.id)
    
    def test_profile_blog_flow(self):
        """Tester le flux complet blog."""
        # Liste
        response = self.client.get(
            reverse('profile_blogue_list', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst'
            })
        )
        self.assertEqual(response.status_code, 200)
        
        # Détail
        response = self.client.get(
            reverse('profile_blogue_detail', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst',
                'slug': self.article.slug
            })
        )
        self.assertEqual(response.status_code, 200)
    
    def test_profile_service_flow(self):
        """Tester le flux complet services."""
        # Liste
        response = self.client.get(
            reverse('profile_service_list', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst'
            })
        )
        self.assertEqual(response.status_code, 200)
        
        # Détail
        response = self.client.get(
            reverse('profile_service_detail', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst',
                'slug': self.service.slug
            })
        )
        self.assertEqual(response.status_code, 200)


class PoolArchitectureTest(TestCase):
    """Tests de l'architecture en pool."""
    
    def setUp(self):
        """Créer deux profils et du contenu partagé."""
        self.client = Client()
        
        self.profile1 = SiteProfile.objects.create(
            first_name="Yama",
            last_name="Sakho",
            profession="Data Analyst",
            is_published=True
        )
        
        self.profile2 = SiteProfile.objects.create(
            first_name="Jane",
            last_name="Smith",
            profession="ML Engineer",
            is_published=True
        )
        
        self.shared_project = Project.objects.create(
            title="Shared Project",
            resume="Available for both",
            content="Content",
            author_name="Author",
            author_email="test@example.com",
            author_profession="Dev"
        )
        
        self.profile1.published_projects.add(self.shared_project)
        self.profile2.published_projects.add(self.shared_project)
    
    def test_same_content_in_multiple_profiles(self):
        """Tester qu'un contenu apparaît dans plusieurs profils."""
        # Profil 1
        response1 = self.client.get(
            reverse('profile_projet_list', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst'
            })
        )
        projects1 = response1.context['projets']
        self.assertEqual(len(projects1), 1)
        
        # Profil 2
        response2 = self.client.get(
            reverse('profile_projet_list', kwargs={
                'nom': 'jane-smith',
                'profession': 'ml-engineer'
            })
        )
        projects2 = response2.context['projets']
        self.assertEqual(len(projects2), 1)
        
        # Même projet
        self.assertEqual(projects1[0].id, projects2[0].id)
    
    def test_content_accessible_from_different_profile_urls(self):
        """Tester l'accès au même contenu via différentes URLs."""
        # URL profil 1
        response1 = self.client.get(
            reverse('profile_projet_detail', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst',
                'slug': self.shared_project.slug
            })
        )
        self.assertEqual(response1.status_code, 200)
        
        # URL profil 2
        response2 = self.client.get(
            reverse('profile_projet_detail', kwargs={
                'nom': 'jane-smith',
                'profession': 'ml-engineer',
                'slug': self.shared_project.slug
            })
        )
        self.assertEqual(response2.status_code, 200)


class URLSlugGenerationTest(TestCase):
    """Tests de génération de slugs dans les URLs."""
    
    def setUp(self):
        """Créer un profil avec caractères spéciaux."""
        self.profile = SiteProfile.objects.create(
            first_name="Jean-Claude",
            last_name="Van Damme",
            profession="Machine Learning Engineer",
            is_published=True
        )
    
    def test_profile_url_contains_correct_slugs(self):
        """Tester que l'URL du profil contient les slugs corrects."""
        url = self.profile.get_absolute_url()
        self.assertIn("jean-claude-van-damme", url)
        self.assertIn("machine-learning-engineer", url)
    
    def test_profile_page_accessible_with_slugs(self):
        """Tester l'accès à la page profil avec slugs."""
        response = self.client.get(
            reverse('profile_home', kwargs={
                'nom': 'jean-claude-van-damme',
                'profession': 'machine-learning-engineer'
            })
        )
        self.assertEqual(response.status_code, 200)


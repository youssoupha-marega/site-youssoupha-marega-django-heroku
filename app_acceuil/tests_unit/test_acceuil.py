"""
Tests pour l'application app_acceuil.

Couvre:
- Modèles: SiteProfile, PublishableContent (via Project pour tests)
- Template tags: profile_nom_slug, profile_profession_slug
- Context processors
- Vues: accueil
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.template import Context, Template
from app_acceuil.models import SiteProfile
from app_projet.models import Project
from app_blog.models import BlogPost
from app_service.models import Service


class SiteProfileModelTest(TestCase):
    """Tests pour le modèle SiteProfile."""
    
    def setUp(self):
        """Créer des profils de test."""
        self.profile = SiteProfile.objects.create(
            first_name="Yama",
            last_name="Sakho",
            profession="Data Analyst",
            email="yama@example.com",
            is_published=True,
            is_default=False
        )
        
        self.default_profile = SiteProfile.objects.create(
            first_name="John",
            last_name="Doe",
            profession="Developer",
            email="john@example.com",
            is_published=True,
            is_default=True
        )
    
    def test_profile_creation(self):
        """Tester la création d'un profil."""
        self.assertEqual(self.profile.first_name, "Yama")
        self.assertEqual(self.profile.last_name, "Sakho")
        self.assertEqual(self.profile.profession, "Data Analyst")
        self.assertTrue(self.profile.is_published)
        self.assertFalse(self.profile.is_default)
    
    def test_profile_slug_generation(self):
        """Tester la génération automatique du slug."""
        # Le slug devrait être généré automatiquement lors de la sauvegarde
        self.assertIsNotNone(self.profile.slug)
        self.assertIn("yama", self.profile.slug.lower())
        self.assertIn("sakho", self.profile.slug.lower())
    
    def test_get_absolute_url_default_profile(self):
        """Tester get_absolute_url pour le profil par défaut."""
        url = self.default_profile.get_absolute_url()
        self.assertEqual(url, "/")
    
    def test_get_absolute_url_non_default_profile(self):
        """Tester get_absolute_url pour un profil non-défaut."""
        url = self.profile.get_absolute_url()
        self.assertIn("nom=yama-sakho", url)
        self.assertIn("profession=data-analyst", url)
    
    def test_get_default_profile_manager(self):
        """Tester la méthode manager get_default_profile."""
        default = SiteProfile.objects.get_default_profile()
        self.assertEqual(default.id, self.default_profile.id)
        self.assertTrue(default.is_default)
    
    def test_str_method(self):
        """Tester la méthode __str__."""
        # is_published=True donne l'emoji 📢
        expected = f"📢 {self.profile.first_name} {self.profile.last_name}"
        self.assertEqual(str(self.profile), expected)


class PublishableContentTest(TestCase):
    """Tests pour le modèle abstrait PublishableContent via Project."""
    
    def setUp(self):
        """Créer un projet de test."""
        self.project = Project.objects.create(
            title="Test Project",
            resume="A test project resume",
            content="Detailed content",
            author_name="Test Author",
            author_email="author@example.com",
            author_profession="Developer"
        )
    
    def test_publishable_content_creation(self):
        """Tester la création de contenu publiable."""
        self.assertEqual(self.project.title, "Test Project")
        self.assertEqual(self.project.resume, "A test project resume")
        self.assertEqual(self.project.author_name, "Test Author")
    
    def test_slug_auto_generation(self):
        """Tester la génération automatique du slug."""
        self.assertIsNotNone(self.project.slug)
        self.assertEqual(self.project.slug, "test-project")
    
    def test_slug_uniqueness(self):
        """Tester l'unicité du slug."""
        project2 = Project.objects.create(
            title="Test Project",  # Même titre
            resume="Another resume",
            content="Content",
            author_name="Author",
            author_email="test@example.com",
            author_profession="Dev"
        )
        # Les slugs doivent être différents
        self.assertNotEqual(self.project.slug, project2.slug)
        self.assertTrue(project2.slug.startswith("test-project"))
    
    def test_created_at_auto_now_add(self):
        """Tester que created_at est défini automatiquement."""
        self.assertIsNotNone(self.project.created_at)
    
    def test_updated_at_auto_now(self):
        """Tester que updated_at est mis à jour."""
        import time
        original_updated = self.project.updated_at
        time.sleep(0.01)  # Petit délai pour s'assurer que le timestamp change
        self.project.title = "Updated Title"
        self.project.save()
        self.assertGreater(self.project.updated_at, original_updated)


class TemplateTagsTest(TestCase):
    """Tests pour les template tags personnalisés."""
    
    def setUp(self):
        """Créer un profil de test."""
        self.profile = SiteProfile.objects.create(
            first_name="Yama",
            last_name="Sakho",
            profession="Data Analyst",
            is_published=True
        )
    
    def test_profile_nom_slug_filter(self):
        """Tester le filtre profile_nom_slug."""
        template = Template("{% load utils %}{{ profile|profile_nom_slug }}")
        context = Context({"profile": self.profile})
        rendered = template.render(context)
        self.assertEqual(rendered, "yama-sakho")
    
    def test_profile_profession_slug_filter(self):
        """Tester le filtre profile_profession_slug."""
        template = Template("{% load utils %}{{ profile|profile_profession_slug }}")
        context = Context({"profile": self.profile})
        rendered = template.render(context)
        self.assertEqual(rendered, "data-analyst")
    
    def test_profile_nom_slug_with_spaces(self):
        """Tester profile_nom_slug avec des espaces et caractères spéciaux."""
        profile = SiteProfile.objects.create(
            first_name="Jean-Claude",
            last_name="Van Damme",
            profession="Actor",
            is_published=True
        )
        template = Template("{% load utils %}{{ profile|profile_nom_slug }}")
        context = Context({"profile": profile})
        rendered = template.render(context)
        self.assertEqual(rendered, "jean-claude-van-damme")
    
    def test_profile_profession_slug_with_spaces(self):
        """Tester profile_profession_slug avec des espaces."""
        profile = SiteProfile.objects.create(
            first_name="Test",
            last_name="User",
            profession="Machine Learning Engineer",
            is_published=True
        )
        template = Template("{% load utils %}{{ profile|profile_profession_slug }}")
        context = Context({"profile": profile})
        rendered = template.render(context)
        self.assertEqual(rendered, "machine-learning-engineer")
    
    def test_profile_url_params_tag(self):
        """Tester le tag profile_url_params."""
        template = Template("{% load utils %}{% profile_url_params profile %}")
        context = Context({"profile": self.profile})
        rendered = template.render(context)
        self.assertIn("nom=yama-sakho", rendered)
        self.assertIn("profession=data-analyst", rendered)
    
    def test_extract_year_filter(self):
        """Tester le filtre extract_year."""
        template = Template("{% load utils %}{{ text|extract_year }}")
        context = Context({"text": "Nordikeau, 2022"})
        rendered = template.render(context)
        self.assertEqual(rendered, "2022")
    
    def test_remove_year_filter(self):
        """Tester le filtre remove_year."""
        template = Template("{% load utils %}{{ text|remove_year }}")
        context = Context({"text": "Nordikeau, 2022"})
        rendered = template.render(context)
        self.assertEqual(rendered, "Nordikeau")


class AccueilViewTest(TestCase):
    """Tests pour la vue d'accueil."""
    
    def setUp(self):
        """Créer des données de test."""
        self.client = Client()
        
        # Créer un profil par défaut
        self.profile = SiteProfile.objects.create(
            first_name="Yama",
            last_name="Sakho",
            profession="Data Analyst",
            is_published=True,
            is_default=True
        )
        
        # Créer des projets
        self.project1 = Project.objects.create(
            title="Project 1",
            resume="Resume 1",
            content="Content 1",
            author_name="Author",
            author_email="test@example.com",
            author_profession="Dev"
        )
        
        # Créer des articles
        self.article1 = BlogPost.objects.create(
            title="Article 1",
            resume="Resume 1",
            content="Content 1",
            author_name="Author",
            author_email="test@example.com",
            author_profession="Writer"
        )
        
        # Créer des services
        self.service1 = Service.objects.create(
            title="Service 1",
            resume="Resume 1",
            content="Content 1",
            author_name="Author",
            author_email="test@example.com",
            author_profession="Consultant"
        )
        
        # Associer au profil
        self.profile.published_projects.add(self.project1)
        self.profile.published_articles.add(self.article1)
        self.profile.published_services.add(self.service1)
    
    def test_accueil_view_status_code(self):
        """Tester que la page d'accueil se charge correctement."""
        response = self.client.get(reverse('acceuil'))
        self.assertEqual(response.status_code, 200)
    
    def test_accueil_view_uses_correct_template(self):
        """Tester que la vue utilise le bon template."""
        response = self.client.get(reverse('acceuil'))
        self.assertTemplateUsed(response, 'app_acceuil/acceuil.html')
    
    def test_accueil_view_context_contains_profile(self):
        """Tester que le contexte contient le profil."""
        response = self.client.get(reverse('acceuil'))
        self.assertIn('site_profile', response.context)
        self.assertEqual(response.context['site_profile'].id, self.profile.id)
    
    def test_accueil_view_context_contains_projects(self):
        """Tester que le contexte contient les projets."""
        response = self.client.get(reverse('acceuil'))
        self.assertIn('projets', response.context)
        self.assertEqual(len(response.context['projets']), 1)
    
    def test_accueil_view_context_contains_articles(self):
        """Tester que le contexte contient les articles."""
        response = self.client.get(reverse('acceuil'))
        self.assertIn('articles', response.context)
        self.assertEqual(len(response.context['articles']), 1)
    
    def test_accueil_view_context_contains_services(self):
        """Tester que le contexte contient les services."""
        response = self.client.get(reverse('acceuil'))
        self.assertIn('services', response.context)
        self.assertEqual(len(response.context['services']), 1)


class ContextProcessorTest(TestCase):
    """Tests pour le context processor."""
    
    def setUp(self):
        """Créer un profil de test."""
        self.client = Client()
        self.profile = SiteProfile.objects.create(
            first_name="Yama",
            last_name="Sakho",
            profession="Data Analyst",
            is_published=True,
            is_default=True
        )
    
    def test_site_profile_in_context(self):
        """Tester que site_profile est disponible dans toutes les pages."""
        response = self.client.get(reverse('acceuil'))
        self.assertIn('site_profile', response.context)
        self.assertIsNotNone(response.context['site_profile'])


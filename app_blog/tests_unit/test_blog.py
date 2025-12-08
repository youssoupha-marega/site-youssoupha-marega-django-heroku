"""
Tests pour l'application app_blog.

Couvre:
- Modèle: BlogPost
- Vues: blogue_list, blogue_detail, profile_blogue_list, profile_blogue_detail
- URLs: racine et profil
"""

from django.test import TestCase, Client
from django.urls import reverse
from app_blog.models import BlogPost
from app_acceuil.models import SiteProfile


class BlogPostModelTest(TestCase):
    """Tests pour le modèle BlogPost."""
    
    def setUp(self):
        """Créer des articles de test."""
        self.article = BlogPost.objects.create(
            title="Introduction au Machine Learning",
            resume="Un guide complet pour débuter en ML",
            content="<p>Contenu détaillé de l'article</p>",
            author_name="Yama Sakho",
            author_email="yama@example.com",
            author_profession="Data Analyst",
            tags="machine learning, python, AI",
            read_time=10
        )
    
    def test_blogpost_creation(self):
        """Tester la création d'un article."""
        self.assertEqual(self.article.title, "Introduction au Machine Learning")
        self.assertEqual(self.article.author_name, "Yama Sakho")
        self.assertEqual(self.article.tags, "machine learning, python, AI")
        self.assertEqual(self.article.read_time, 10)
    
    def test_blogpost_slug_generation(self):
        """Tester la génération du slug."""
        self.assertEqual(self.article.slug, "introduction-au-machine-learning")
    
    def test_blogpost_get_absolute_url(self):
        """Tester get_absolute_url."""
        url = self.article.get_absolute_url()
        expected = reverse('blogue_detail', kwargs={'slug': self.article.slug})
        self.assertEqual(url, expected)
    
    def test_blogpost_str_method(self):
        """Tester la méthode __str__."""
        self.assertEqual(str(self.article), "Introduction au Machine Learning")
    
    def test_blogpost_default_read_time(self):
        """Tester la valeur par défaut du temps de lecture."""
        article = BlogPost.objects.create(
            title="Quick Post",
            resume="Resume",
            content="Content",
            author_name="Author",
            author_email="test@example.com",
            author_profession="Writer"
        )
        self.assertEqual(article.read_time, 5)  # Valeur par défaut


class BlogListViewTest(TestCase):
    """Tests pour la vue de liste des articles (racine)."""
    
    def setUp(self):
        """Créer des articles de test."""
        self.client = Client()
        
        self.article1 = BlogPost.objects.create(
            title="Article 1",
            resume="Resume 1",
            content="Content 1",
            author_name="Author",
            author_email="test@example.com",
            author_profession="Writer"
        )
        
        self.article2 = BlogPost.objects.create(
            title="Article 2",
            resume="Resume 2",
            content="Content 2",
            author_name="Author",
            author_email="test@example.com",
            author_profession="Writer"
        )
    
    def test_list_view_status_code(self):
        """Tester que la page de liste se charge."""
        response = self.client.get(reverse('blogue_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_list_view_uses_correct_template(self):
        """Tester que la vue utilise le bon template."""
        response = self.client.get(reverse('blogue_list'))
        self.assertTemplateUsed(response, 'app_blog/list.html')
    
    def test_list_view_contains_articles(self):
        """Tester que la vue contient les articles."""
        response = self.client.get(reverse('blogue_list'))
        self.assertIn('articles', response.context)
        self.assertEqual(len(response.context['articles']), 2)
    
    def test_list_view_articles_ordered_by_date(self):
        """Tester que les articles sont triés par date."""
        response = self.client.get(reverse('blogue_list'))
        articles = list(response.context['articles'])
        self.assertEqual(len(articles), 2)
        self.assertGreaterEqual(articles[0].created_at, articles[1].created_at)


class BlogDetailViewTest(TestCase):
    """Tests pour la vue de détail d'un article (racine)."""
    
    def setUp(self):
        """Créer un article de test."""
        self.client = Client()
        
        self.article = BlogPost.objects.create(
            title="Test Article",
            resume="Test resume",
            content="Test content",
            author_name="Author",
            author_email="test@example.com",
            author_profession="Writer"
        )
    
    def test_detail_view_status_code(self):
        """Tester que la page de détail se charge."""
        response = self.client.get(
            reverse('blogue_detail', kwargs={'slug': self.article.slug})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_detail_view_uses_correct_template(self):
        """Tester que la vue utilise le bon template."""
        response = self.client.get(
            reverse('blogue_detail', kwargs={'slug': self.article.slug})
        )
        self.assertTemplateUsed(response, 'app_blog/detail.html')
    
    def test_detail_view_contains_article(self):
        """Tester que la vue contient l'article."""
        response = self.client.get(
            reverse('blogue_detail', kwargs={'slug': self.article.slug})
        )
        self.assertEqual(response.context['article'].id, self.article.id)
    
    def test_detail_view_404_for_invalid_slug(self):
        """Tester que la vue retourne 404 pour un slug invalide."""
        response = self.client.get(
            reverse('blogue_detail', kwargs={'slug': 'slug-inexistant'})
        )
        self.assertEqual(response.status_code, 404)


class ProfileBlogViewsTest(TestCase):
    """Tests pour les vues d'articles avec contexte profil."""
    
    def setUp(self):
        """Créer un profil et des articles de test."""
        self.client = Client()
        
        # Créer un profil
        self.profile = SiteProfile.objects.create(
            first_name="Yama",
            last_name="Sakho",
            profession="Data Analyst",
            is_published=True,
            is_default=False
        )
        
        # Créer des articles
        self.article1 = BlogPost.objects.create(
            title="Article 1",
            resume="Resume 1",
            content="Content 1",
            author_name="Yama Sakho",
            author_email="yama@example.com",
            author_profession="Data Analyst"
        )
        
        self.article2 = BlogPost.objects.create(
            title="Article 2",
            resume="Resume 2",
            content="Content 2",
            author_name="Yama Sakho",
            author_email="yama@example.com",
            author_profession="Data Analyst"
        )
        
        # Associer les articles au profil
        self.profile.published_articles.add(self.article1, self.article2)
    
    def test_profile_list_view_status_code(self):
        """Tester que la liste profil se charge."""
        response = self.client.get(
            reverse('profile_blogue_list', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst'
            })
        )
        self.assertEqual(response.status_code, 200)
    
    def test_profile_list_view_contains_profile_articles(self):
        """Tester que la liste contient les articles du profil."""
        response = self.client.get(
            reverse('profile_blogue_list', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst'
            })
        )
        self.assertIn('articles', response.context)
        self.assertEqual(len(response.context['articles']), 2)
    
    def test_profile_list_view_contains_profile_context(self):
        """Tester que le contexte contient le profil."""
        response = self.client.get(
            reverse('profile_blogue_list', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst'
            })
        )
        self.assertIn('site_profile', response.context)
        self.assertEqual(response.context['site_profile'].id, self.profile.id)
    
    def test_profile_detail_view_status_code(self):
        """Tester que le détail profil se charge."""
        response = self.client.get(
            reverse('profile_blogue_detail', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst',
                'slug': self.article1.slug
            })
        )
        self.assertEqual(response.status_code, 200)
    
    def test_profile_detail_view_contains_article(self):
        """Tester que le détail contient l'article."""
        response = self.client.get(
            reverse('profile_blogue_detail', kwargs={
                'nom': 'yama-sakho',
                'profession': 'data-analyst',
                'slug': self.article1.slug
            })
        )
        self.assertEqual(response.context['article'].id, self.article1.id)
    
    def test_profile_detail_404_if_profile_not_found(self):
        """Tester 404 si le profil n'existe pas."""
        response = self.client.get(
            reverse('profile_blogue_detail', kwargs={
                'nom': 'invalid-name',
                'profession': 'invalid-profession',
                'slug': self.article1.slug
            })
        )
        self.assertEqual(response.status_code, 404)


class BlogURLTest(TestCase):
    """Tests pour les URLs des articles."""
    
    def test_root_list_url_resolves(self):
        """Tester que l'URL de liste racine est correcte."""
        url = reverse('blogue_list')
        self.assertEqual(url, '/blogue/')
    
    def test_root_detail_url_resolves(self):
        """Tester que l'URL de détail racine est correcte."""
        url = reverse('blogue_detail', kwargs={'slug': 'test-article'})
        self.assertEqual(url, '/blogue/test-article/')
    
    def test_profile_list_url_resolves(self):
        """Tester que l'URL de liste profil est correcte."""
        url = reverse('profile_blogue_list', kwargs={
            'nom': 'yama-sakho',
            'profession': 'data-analyst'
        })
        self.assertEqual(url, '/profil/nom=yama-sakho&profession=data-analyst/blog/')
    
    def test_profile_detail_url_resolves(self):
        """Tester que l'URL de détail profil est correcte."""
        url = reverse('profile_blogue_detail', kwargs={
            'nom': 'yama-sakho',
            'profession': 'data-analyst',
            'slug': 'test-article'
        })
        self.assertEqual(
            url,
            '/profil/nom=yama-sakho&profession=data-analyst/blog/test-article/'
        )


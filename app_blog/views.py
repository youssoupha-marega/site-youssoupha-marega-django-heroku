"""
Vues pour l'application blog.

Utilise les classes de base ProfileBasedListView et ProfileBasedDetailView
pour éliminer la duplication de code.
"""

from app_acceuil.base_views import ProfileBasedListView, ProfileBasedDetailView
from .models import BlogPost


class BlogListView(ProfileBasedListView):
    """Vue de liste des articles de blog pour un profil."""
    
    model = BlogPost
    template_name = 'app_blog/list.html'
    context_object_name = 'articles'
    profile_featured_attr = 'published_articles'


class BlogDetailView(ProfileBasedDetailView):
    """Vue de détail d'un article de blog."""
    
    model = BlogPost
    template_name = 'app_blog/detail.html'
    context_object_name = 'article'


# Vues fonctionnelles pour compatibilité avec les URLs existantes
def blogue_list(request, nom=None, profession=None):
    """Wrapper fonctionnel pour BlogListView."""
    view = BlogListView.as_view()
    return view(request, nom=nom, profession=profession)


def blogue_detail(request, slug, nom=None, profession=None):
    """Wrapper fonctionnel pour BlogDetailView."""
    view = BlogDetailView.as_view()
    return view(request, slug=slug, nom=nom, profession=profession)

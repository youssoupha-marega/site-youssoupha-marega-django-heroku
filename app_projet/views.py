"""
Vues pour l'application projets.

Utilise les classes de base ProfileBasedListView et ProfileBasedDetailView
pour éliminer la duplication de code.
"""

from app_acceuil.base_views import ProfileBasedListView, ProfileBasedDetailView
from .models import Project


class ProjectListView(ProfileBasedListView):
    """Vue de liste des projets pour un profil."""
    
    model = Project
    template_name = 'app_projet/list.html'
    context_object_name = 'projets'
    profile_featured_attr = 'published_projects'


class ProjectDetailView(ProfileBasedDetailView):
    """Vue de détail d'un projet."""
    
    model = Project
    template_name = 'app_projet/detail.html'
    context_object_name = 'projet'


# Vues fonctionnelles pour compatibilité avec les URLs existantes
def projet_list(request, nom=None, profession=None):
    """Wrapper fonctionnel pour ProjectListView."""
    view = ProjectListView.as_view()
    return view(request, nom=nom, profession=profession)


def projet_detail(request, slug, nom=None, profession=None):
    """Wrapper fonctionnel pour ProjectDetailView."""
    view = ProjectDetailView.as_view()
    return view(request, slug=slug, nom=nom, profession=profession)
    
    # Charger le profil pour le contexte
    if profile_slug:
        site_profile = get_object_or_404(SiteProfile, slug=profile_slug, is_published=True)
    else:
        site_profile = SiteProfile.objects.filter(is_default=True, is_published=True).first()
        if not site_profile:
            site_profile = SiteProfile.objects.filter(is_published=True).first()
    
    return render(request, 'app_projet/detail.html', {'projet': projet, 'site_profile': site_profile})

from django.shortcuts import render, get_object_or_404
from .models import BlogPost
from app_acceuil.models import SiteProfile

def blogue_list(request, nom=None, profession=None):
    """Liste des articles de blog pour le profil par défaut ou un profil spécifique"""
    from django.utils.text import slugify
    
    # Construire le slug du profil à partir des paramètres
    profile_slug = f"{nom}-{profession}" if nom and profession else None
    
    if profile_slug:
        # Profil spécifique avec slug
        site_profile = get_object_or_404(
            SiteProfile.objects.prefetch_related('published_articles'),
            slug=profile_slug,
            is_published=True
        )
        # Afficher uniquement les articles publiés pour ce profil
        if site_profile.published_articles.exists():
            articles = site_profile.published_articles.filter(is_published=True)
        else:
            articles = BlogPost.objects.none()
    else:
        # Profil par défaut
        site_profile = SiteProfile.objects.prefetch_related('published_articles').filter(
            is_default=True, is_published=True
        ).first()
        
        if not site_profile:
            site_profile = SiteProfile.objects.prefetch_related('published_articles').filter(
                is_published=True
            ).first()
        
        # Afficher les articles publiés pour ce profil ou tous si aucun sélectionné
        if site_profile and site_profile.published_articles.exists():
            articles = site_profile.published_articles.filter(is_published=True)
        else:
            articles = BlogPost.objects.filter(is_published=True)
    
    return render(request, 'app_blog/list.html', {'articles': articles, 'site_profile': site_profile})

def blogue_detail(request, slug, nom=None, profession=None):
    """Détail d'un article de blog"""
    from django.utils.text import slugify
    
    article = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    # Construire le slug du profil à partir des paramètres
    profile_slug = f"{nom}-{profession}" if nom and profession else None
    
    # Charger le profil pour le contexte
    if profile_slug:
        site_profile = get_object_or_404(SiteProfile, slug=profile_slug, is_published=True)
    else:
        site_profile = SiteProfile.objects.filter(is_default=True, is_published=True).first()
        if not site_profile:
            site_profile = SiteProfile.objects.filter(is_published=True).first()
    
    return render(request, 'app_blog/detail.html', {'article': article, 'site_profile': site_profile})

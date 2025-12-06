from django.shortcuts import render, get_object_or_404
from .models import Service
from app_acceuil.models import SiteProfile

def service_list(request, nom=None, profession=None):
    """Liste des services pour le profil par défaut ou un profil spécifique"""
    from django.utils.text import slugify
    
    # Construire le slug du profil à partir des paramètres
    profile_slug = f"{nom}-{profession}" if nom and profession else None
    
    if profile_slug:
        # Profil spécifique avec slug
        site_profile = get_object_or_404(
            SiteProfile.objects.prefetch_related('published_services'),
            slug=profile_slug,
            is_published=True
        )
        # Afficher uniquement les services publiés pour ce profil
        if site_profile.published_services.exists():
            services = site_profile.published_services.filter(is_published=True)
        else:
            services = Service.objects.none()
    else:
        # Profil par défaut
        site_profile = SiteProfile.objects.prefetch_related('published_services').filter(
            is_default=True, is_published=True
        ).first()
        
        if not site_profile:
            site_profile = SiteProfile.objects.prefetch_related('published_services').filter(
                is_published=True
            ).first()
        
        # Afficher les services publiés pour ce profil ou tous si aucun sélectionné
        if site_profile and site_profile.published_services.exists():
            services = site_profile.published_services.filter(is_published=True)
        else:
            services = Service.objects.filter(is_published=True)
    
    return render(request, 'app_service/list.html', {'services': services, 'site_profile': site_profile})

def service_detail(request, slug, nom=None, profession=None):
    """Détail d'un service"""
    from django.utils.text import slugify
    
    service = get_object_or_404(Service, slug=slug, is_published=True)
    
    # Construire le slug du profil à partir des paramètres
    profile_slug = f"{nom}-{profession}" if nom and profession else None
    
    # Charger le profil pour le contexte
    if profile_slug:
        site_profile = get_object_or_404(SiteProfile, slug=profile_slug, is_published=True)
    else:
        site_profile = SiteProfile.objects.filter(is_default=True, is_published=True).first()
        if not site_profile:
            site_profile = SiteProfile.objects.filter(is_published=True).first()
    
    return render(request, 'app_service/detail.html', {'service': service, 'site_profile': site_profile})

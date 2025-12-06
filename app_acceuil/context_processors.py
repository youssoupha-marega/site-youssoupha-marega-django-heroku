# app_acceuil/context_processors.py
from .models import SiteProfile
from django.db import DatabaseError, OperationalError


def menu_items(request):
    """Generate dynamic menu items based on the current profile"""
    try:
        # Essayer de détecter le profil depuis les paramètres du chemin
        nom = None
        profession = None
        if request.resolver_match:
            nom = request.resolver_match.kwargs.get('nom')
            profession = request.resolver_match.kwargs.get('profession')
        
        profile_slug = f"{nom}-{profession}" if nom and profession else None
        
        if profile_slug:
            # Profil spécifique
            profile = SiteProfile.objects.filter(slug=profile_slug, is_published=True).first()
        else:
            # Profil par défaut
            profile = SiteProfile.objects.filter(is_default=True, is_published=True).first()
        
        if profile:
            projects_label = profile.projects_navbar_label if profile.projects_navbar_label else "Projets"
            blog_label = profile.blog_navbar_label if profile.blog_navbar_label else "Blogue"
            services_label = profile.services_navbar_label if profile.services_navbar_label else "Services"
            
            # Générer les URLs en fonction du profil
            if profile.is_default:
                items = [
                    {"name": "acceuil", "label": "Accueil", "url": "/"},
                    {"name": "service_list", "label": services_label, "url": "/services/"},
                    {"name": "projet_list", "label": projects_label, "url": "/projets/"},
                    {"name": "blogue_list", "label": blog_label, "url": "/blogue/"},
                ]
            else:
                # Utiliser les paramètres dans le chemin
                from django.utils.text import slugify
                nom_slug = slugify(f"{profile.first_name}-{profile.last_name}")
                profession_slug = slugify(profile.profession) if profile.profession else "profil"
                base_path = f"/profil/nom={nom_slug}&profession={profession_slug}"
                
                items = [
                    {"name": "profile_home", "label": "Accueil", "url": f"{base_path}/"},
                    {"name": "profile_service_list", "label": services_label, "url": f"{base_path}/services/"},
                    {"name": "profile_projet_list", "label": projects_label, "url": f"{base_path}/projets/"},
                    {"name": "profile_blogue_list", "label": blog_label, "url": f"{base_path}/blog/"},
                ]
        else:
            items = [
                {"name": "acceuil", "label": "Accueil", "url": "/"},
                {"name": "service_list", "label": "Services", "url": "/services/"},
                {"name": "projet_list", "label": "Projets", "url": "/projets/"},
                {"name": "blogue_list", "label": "Blogue", "url": "/blogue/"},
            ]
    except (OperationalError, DatabaseError):
        items = [
            {"name": "acceuil", "label": "Accueil", "url": "/"},
            {"name": "service_list", "label": "Services", "url": "/services/"},
            {"name": "projet_list", "label": "Projets", "url": "/projets/"},
            {"name": "blogue_list", "label": "Blogue", "url": "/blogue/"},
        ]
    
    return {'menu_items': items}


def site_profile(request):
    """Expose the current SiteProfile instance as `site_profile` in templates.

    This context processor is defensive: during initial migrations the
    `app_acceuil_siteprofile` table or new columns (like `site_title`) may
    not exist yet which leads to OperationalError. Catch DB errors and
    return `None` so templates can still render (they already have fallbacks).
    """
    try:
        # Essayer de détecter le profil depuis les paramètres du chemin
        nom = None
        profession = None
        if request.resolver_match:
            nom = request.resolver_match.kwargs.get('nom')
            profession = request.resolver_match.kwargs.get('profession')
        
        profile_slug = f"{nom}-{profession}" if nom and profession else None
        
        if profile_slug:
            # Profil spécifique
            profile = SiteProfile.objects.filter(slug=profile_slug, is_published=True).first()
        else:
            # Profil par défaut
            profile = SiteProfile.objects.filter(is_default=True, is_published=True).first()
    except (OperationalError, DatabaseError):
        # Database not ready / migrations not applied yet. Return no profile.
        profile = None
    return {"site_profile": profile}

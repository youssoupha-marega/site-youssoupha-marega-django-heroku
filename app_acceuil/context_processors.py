# app_acceuil/context_processors.py
from .models import SiteProfile
from django.db import DatabaseError, OperationalError


def menu_items(request):
    return {
        'menu_items': [
            {"name": "acceuil", "label": "Acceuil"},
            {"name": "service_list", "label": "Services"},
            {"name": "projet_list", "label": "Projet"},
            {"name": "blogue_list", "label": "Blogue"},
        ]
    }


def site_profile(request):
    """Expose the first SiteProfile instance as `site_profile` in templates.

    This context processor is defensive: during initial migrations the
    `app_acceuil_siteprofile` table or new columns (like `site_title`) may
    not exist yet which leads to OperationalError. Catch DB errors and
    return `None` so templates can still render (they already have fallbacks).
    """
    try:
        profile = SiteProfile.objects.first()
    except (OperationalError, DatabaseError):
        # Database not ready / migrations not applied yet. Return no profile.
        profile = None
    return {"site_profile": profile}

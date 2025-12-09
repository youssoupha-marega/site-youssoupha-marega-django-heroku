"""
Service layer for business logic related to site profiles and content.

This module centralizes the logic for retrieving featured content, determining
default profiles, and building context data for views.
"""

from typing import Dict, Any, Optional
from app_content.models import Content
from .models import SiteProfile


class ProfileService:
    """Service for handling profile-related business logic."""

    @staticmethod
    def get_featured_projects(site_profile: Optional[SiteProfile], limit: int = 3):
        """
        Get featured projects for a given profile.

        Args:
            site_profile: The SiteProfile instance or None.
            limit: Maximum number of projects to return.

        Returns:
            QuerySet of Content instances with content_type='project'.
        """
        # Retourner tous les projets (limités)
        return Content.objects.filter(content_type='project').order_by('-created_at')[:limit]

    @staticmethod
    def get_featured_articles(site_profile: Optional[SiteProfile], limit: int = 3):
        """
        Get featured blog articles for a given profile.

        Args:
            site_profile: The SiteProfile instance or None.
            limit: Maximum number of articles to return.

        Returns:
            QuerySet of Content instances with content_type='blog'.
        """
        # Retourner tous les articles (limités)
        return Content.objects.filter(content_type='blog').order_by('-created_at')[:limit]

    @staticmethod
    def get_featured_services(site_profile: Optional[SiteProfile], limit: int = 3):
        """
        Get featured services for a given profile.

        Args:
            site_profile: The SiteProfile instance or None.
            limit: Maximum number of services to return.

        Returns:
            QuerySet of Content instances with content_type='service'.
        """
        # Retourner tous les services (limités)
        return Content.objects.filter(content_type='service').order_by('-created_at')[:limit]

    @staticmethod
    def build_profile_context(site_profile: Optional[SiteProfile]) -> Dict[str, Any]:
        """
        Build the context dictionary for rendering profile-based templates.

        Args:
            site_profile: The SiteProfile instance or None.

        Returns:
            Dictionary with 'projets', 'articles', 'services', and 'site_profile' keys.
        """
        return {
            'projets': ProfileService.get_featured_projects(site_profile),
            'articles': ProfileService.get_featured_articles(site_profile),
            'services': ProfileService.get_featured_services(site_profile),
            'site_profile': site_profile,
        }

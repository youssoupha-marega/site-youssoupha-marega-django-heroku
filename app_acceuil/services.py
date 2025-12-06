"""
Service layer for business logic related to site profiles and content.

This module centralizes the logic for retrieving featured content, determining
default profiles, and building context data for views.
"""

from typing import Dict, Any, Optional
from app_projet.models import Project
from app_blog.models import BlogPost
from app_service.models import Service
from .models import SiteProfile


class ProfileService:
    """Service for handling profile-related business logic."""

    @staticmethod
    def get_featured_projects(site_profile: Optional[SiteProfile], limit: int = 3):
        """
        Get featured projects for a given profile.

        Args:
            site_profile: The SiteProfile instance or None.
            limit: Maximum number of projects to return if using fallback.

        Returns:
            QuerySet of Project instances.
        """
        if site_profile and site_profile.featured_projects.exists():
            return site_profile.featured_projects.all()
        elif site_profile and site_profile.published_projects.exists():
            return site_profile.published_projects.all()[:limit]
        else:
            # Fallback: retourner tous les projets (limités)
            return Project.objects.all()[:limit]

    @staticmethod
    def get_featured_articles(site_profile: Optional[SiteProfile], limit: int = 3):
        """
        Get featured blog articles for a given profile.

        Args:
            site_profile: The SiteProfile instance or None.
            limit: Maximum number of articles to return if using fallback.

        Returns:
            QuerySet of BlogPost instances.
        """
        if site_profile and site_profile.featured_articles.exists():
            return site_profile.featured_articles.all()
        elif site_profile and site_profile.published_articles.exists():
            return site_profile.published_articles.all()[:limit]
        else:
            # Fallback: retourner tous les articles (limités)
            return BlogPost.objects.all()[:limit]

    @staticmethod
    def get_featured_services(site_profile: Optional[SiteProfile], limit: int = 3):
        """
        Get featured services for a given profile.

        Args:
            site_profile: The SiteProfile instance or None.
            limit: Maximum number of services to return if using fallback.

        Returns:
            QuerySet of Service instances.
        """
        if site_profile and site_profile.featured_services.exists():
            return site_profile.featured_services.all()
        elif site_profile and site_profile.published_services.exists():
            return site_profile.published_services.all()[:limit]
        else:
            # Fallback: retourner tous les services (limités)
            return Service.objects.all()[:limit]

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

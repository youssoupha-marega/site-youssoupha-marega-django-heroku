from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from app_acceuil.base_models import PublishableContent, PublishableContentManager


CONTENT_TYPE_CHOICES = [
    ('project', _('Projet')),
    ('blog', _('Article de Blog')),
    ('service', _('Service')),
]


class Content(PublishableContent):
    """
    Modèle générique pour tous les types de contenu (Projets, Articles, Services).
    
    Le type de contenu (content_type) détermine :
    - L'icône, couleur et label affichés
    - L'URL de détail
    - Les champs spécifiques utilisés
    
    Hérite de PublishableContent pour les champs communs :
    title, slug, resume, is_published, featured, author_*, dates, etc.
    """
    
    # Type de contenu (détermine l'icône, couleur, URL, etc)
    content_type = models.CharField(
        max_length=20,
        choices=CONTENT_TYPE_CHOICES,
        default='project',
        verbose_name=_("Type de contenu"),
        help_text=_("Sélectionnez le type : Projet, Article ou Service")
    )
    
    # Contenu principal
    content = RichTextUploadingField(
        verbose_name=_("Contenu détaillé"),
        help_text=_("Description complète avec images, mise en forme, etc.")
    )
    
    # Image principale
    main_image = models.ImageField(
        upload_to='content/%Y/%m/',
        blank=True,
        null=True,
        verbose_name=_("Image principale")
    )
    
    # Champs optionnels - Projets
    github_url = models.URLField(
        blank=True,
        verbose_name=_("Lien GitHub (projets)"),
        help_text=_("URL du dépôt GitHub du projet")
    )
    demo_url = models.URLField(
        blank=True,
        verbose_name=_("Lien démo (projets)"),
        help_text=_("URL de la démo ou du site en ligne")
    )
    
    # Champs optionnels - Services
    calendly_url = models.URLField(
        blank=True,
        verbose_name=_("Lien Calendly (services)"),
        help_text=_("URL pour réserver une consultation")
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Prix (services)"),
        help_text=_("Prix du service (format: 99.99)")
    )
    duration = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Durée (services)"),
        help_text=_("Exemple: '1 heure', '2 jours', 'Sur devis'")
    )
    
    # Manager customisé pour filtrer par type
    objects = PublishableContentManager()
    
    def get_absolute_url(self):
        """Génère l'URL selon le type de contenu"""
        type_routes = {
            'project': 'projets',
            'blog': 'blog',
            'service': 'services'
        }
        route = type_routes.get(self.content_type, 'contenu')
        return reverse('content_detail', args=[route, self.slug])
    
    def get_type_display_info(self):
        """Retourne les infos d'affichage selon le type"""
        type_config = {
            'project': {
                'icon': 'fa-rocket',
                'color': '#2c5282',
                'label': 'Projet'
            },
            'blog': {
                'icon': 'fa-pen-fancy',
                'color': '#4a90a4',
                'label': 'Article'
            },
            'service': {
                'icon': 'fa-tools',
                'color': '#744210',
                'label': 'Service'
            }
        }
        return type_config.get(self.content_type, type_config['project'])
    
    class Meta:
        verbose_name = _("Contenu")
        verbose_name_plural = _("Contenu")
        ordering = ['-created_at']

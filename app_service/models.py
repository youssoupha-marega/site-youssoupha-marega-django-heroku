from django.db import models
from django.urls import reverse
from app_acceuil.base_models import PublishableContent, PublishableContentManager


class Service(PublishableContent):
    """
    Modèle pour les services proposés.
    
    Hérite de PublishableContent pour les champs communs (title, slug, resume,
    is_published, featured, author_*, dates, etc.).
    
    Ajoute uniquement les champs spécifiques aux services.
    """
    
    # Champs spécifiques aux services
    content = models.TextField(verbose_name="Description complète du service")
    calendly_url = models.URLField(
        max_length=500, 
        blank=True, 
        verbose_name="Lien Calendly pour réservation"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True,
        verbose_name="Prix (optionnel)"
    )
    duration = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name="Durée (ex: '1 heure', '2 jours')"
    )
    
    objects = PublishableContentManager()

    def get_absolute_url(self):
        """Retourne l'URL de la page de détail du service."""
        return reverse('service_detail', kwargs={'slug': self.slug})

    class Meta(PublishableContent.Meta):
        verbose_name = "Service"
        verbose_name_plural = "Services"
        # Hérite ordering = ['-created_at'] de PublishableContent

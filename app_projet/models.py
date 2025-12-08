from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from app_acceuil.base_models import PublishableContent, PublishableContentManager


class Project(PublishableContent):
    """
    Modèle pour les projets du portfolio.
    
    Hérite de PublishableContent pour les champs communs (title, slug, resume,
    is_published, featured, author_*, dates, etc.).
    
    Ajoute uniquement les champs spécifiques aux projets.
    """
    
    # Champs spécifiques aux projets
    content = RichTextUploadingField(verbose_name="Contenu détaillé")
    main_image = models.ImageField(
        upload_to='projets/', 
        blank=True, 
        null=True, 
        verbose_name="Image principale"
    )
    github_url = models.URLField(blank=True, verbose_name="Lien GitHub")
    demo_url = models.URLField(blank=True, verbose_name="Lien démo")
    
    objects = PublishableContentManager()

    def get_absolute_url(self):
        """Retourne l'URL de la page de détail du projet."""
        return reverse('projet_detail', kwargs={'slug': self.slug})

    class Meta(PublishableContent.Meta):
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        # Hérite ordering = ['-created_at'] de PublishableContent

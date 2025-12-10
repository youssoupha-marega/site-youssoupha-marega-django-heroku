"""
Modèles de base abstraits pour partager la logique commune entre
Project, BlogPost et Service.
"""

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField


class PublishableContent(models.Model):
    """
    Modèle abstrait pour tout contenu publiable (projets, articles, services).
    
    Fournit les champs et comportements communs :
    - Publication/dépublication
    - Featured/mise en avant
    - Slug automatique
    - Métadonnées d'auteur
    - Dates de création/modification
    """
    
    title = models.CharField(max_length=200, verbose_name=_("Titre"))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_("Slug"))
    resume = RichTextUploadingField(verbose_name=_("Résumé"))
    
    # Métadonnées
    author_name = models.CharField(
        max_length=100, 
        verbose_name=_("Nom de l'auteur"), 
        default="Youssoupha Marega"
    )
    author_email = models.EmailField(
        verbose_name=_("Email de l'auteur"), 
        default="contact@youssouphamarega.com"
    )
    author_profession = models.CharField(
        max_length=100, 
        verbose_name=_("Profession de l'auteur"), 
        default="Data Scientist"
    )
    
    # Dates
    published_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de publication"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de création"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Date de modification"))
    
    class Meta:
        abstract = True
        ordering = ['-published_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """Génère automatiquement le slug si non fourni."""
        if not self.slug:
            self.slug = slugify(self.title)
            # Assurer l'unicité du slug
            original_slug = self.slug
            counter = 1
            while self.__class__.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)


class PublishableContentManager(models.Manager):
    """Manager commun pour tout contenu publiable."""
    
    def all_items(self):
        """Retourne tous les items disponibles pour tous les profils."""
        return self.all()
    
    def get_by_slug(self, slug):
        """Récupère un élément par son slug."""
        return self.get(slug=slug)

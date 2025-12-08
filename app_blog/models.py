from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from app_acceuil.base_models import PublishableContent, PublishableContentManager


class BlogPost(PublishableContent):
    """
    Modèle pour les articles de blog.
    
    Hérite de PublishableContent pour les champs communs (title, slug, resume,
    is_published, featured, author_*, dates, etc.).
    
    Ajoute uniquement les champs spécifiques aux articles.
    """
    
    # Champs spécifiques aux articles de blog
    content = RichTextUploadingField(verbose_name="Contenu de l'article")
    main_image = models.ImageField(
        upload_to='blog/', 
        blank=True, 
        null=True, 
        verbose_name="Image principale"
    )
    tags = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name="Tags (séparés par des virgules)"
    )
    read_time = models.IntegerField(
        default=5, 
        verbose_name="Temps de lecture (minutes)"
    )
    
    objects = PublishableContentManager()

    def get_absolute_url(self):
        """Retourne l'URL de la page de détail de l'article."""
        return reverse('blogue_detail', kwargs={'slug': self.slug})

    class Meta(PublishableContent.Meta):
        verbose_name = "Article de blog"
        verbose_name_plural = "Articles de blog"
        # Hérite ordering = ['-created_at'] de PublishableContent

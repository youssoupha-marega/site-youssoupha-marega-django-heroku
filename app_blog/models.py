from django.db import models
from django.utils.text import slugify

from ckeditor_uploader.fields import RichTextUploadingField

class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    resume = models.TextField(verbose_name="Résumé")
    content = RichTextUploadingField(verbose_name="Contenu")
    published_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de publication")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    is_published = models.BooleanField(default=True, verbose_name="Est publié")
    featured = models.BooleanField(default=False, verbose_name="Article mis en avant")
    author_name = models.CharField(max_length=100, verbose_name="Nom de l'auteur", default="Youssoupha Marega")
    author_email = models.EmailField(verbose_name="Email de l'auteur", default="contact@youssouphamarega.com")
    author_profession = models.CharField(max_length=100, verbose_name="Profession de l'auteur", default="Data Scientist")
    main_image = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name="Image principale")

    class Meta:
        verbose_name = "Article de blog"
        verbose_name_plural = "Articles de blog"
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

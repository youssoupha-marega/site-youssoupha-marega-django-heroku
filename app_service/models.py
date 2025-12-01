from django.db import models
from django.utils.text import slugify

class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    resume = models.TextField(verbose_name="Résumé")
    content = models.TextField(verbose_name="Description complète")
    calendly_url = models.URLField(max_length=500, blank=True, verbose_name="Lien Calendly")
    is_published = models.BooleanField(default=True, verbose_name="Est publié")
    featured = models.BooleanField(default=False, verbose_name="Service mis en avant")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

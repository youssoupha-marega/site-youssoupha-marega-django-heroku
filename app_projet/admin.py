from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'published_at', 'updated_at')
    list_filter = ('published_at', 'author_name')
    search_fields = ('title', 'resume', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('title', 'slug', 'resume')
        }),
        ('Contenu', {
            'fields': ('content', 'main_image')
        }),
        ('Liens', {
            'fields': ('github_url', 'demo_url')
        }),
        ('Auteur', {
            'fields': ('author_name', 'author_email', 'author_profession')
        }),
        ('Dates', {
            'fields': ('published_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_prepopulated_fields(self, request, obj=None):
        """Désactive prepopulated_fields en édition."""
        if obj:  # En édition, pas de prepopulated
            return {}
        return self.prepopulated_fields  # Création, prepopulated actif
    
    def get_readonly_fields(self, request, obj=None):
        """Slug readonly en édition, dates toujours readonly."""
        if obj:  # En édition - slug devient readonly
            return ('slug', 'created_at', 'updated_at', 'published_at')
        return ('created_at', 'updated_at', 'published_at')  # Création - slug éditable via prepopulated

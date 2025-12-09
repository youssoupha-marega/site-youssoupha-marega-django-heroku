from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.db import models
from .models import Content, CONTENT_TYPE_CHOICES


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """
    Admin pour la gestion unifiée de tous les types de contenu.
    Les champs affichés changent dynamiquement selon le type de contenu.
    """
    
    list_display = ['title', 'content_type_badge', 'created_at']
    list_filter = ['content_type', 'created_at']
    search_fields = ['title', 'slug', 'resume']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    # Personnalisation formulaire
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget()}
    }
    
    fieldsets = None  # Sera généré dynamiquement selon le type
    
    def get_fieldsets(self, request, obj=None):
        """Retourne les fieldsets dynamiques selon le type de contenu"""
        
        # Fieldset commun pour tous les types
        common_fieldset = (
            _("Informations générales"), {
                'fields': ('title', 'slug', 'content_type', 'resume', 'content')
            }
        )
        
        # Fieldset image
        image_fieldset = (
            _("Image principale"), {
                'fields': ('main_image',),
                'classes': ('collapse',)
            }
        )
        
        # Champs spécifiques aux projets
        project_fieldset = (
            _("Informations du projet"), {
                'fields': ('github_url', 'demo_url'),
                'classes': ('collapse',)
            }
        )
        
        # Champs spécifiques aux services
        service_fieldset = (
            _("Informations du service"), {
                'fields': ('calendly_url', 'price', 'duration'),
                'classes': ('collapse',)
            }
        )
        
        # Champs de publication
        publication_fieldset = (
            _("Dates"), {
                'fields': ('created_at', 'updated_at'),
                'classes': ('collapse',)
            }
        )
        
        # Champs d'auteur (métadonnées)
        author_fieldset = (
            _("Auteur et Métadonnées"), {
                'fields': (
                    'author_name', 'author_title', 'author_description',
                    'author_avatar', 'author_avatar_alt'
                ),
                'classes': ('collapse',)
            }
        )
        
        # Contrôles de contenu
        controls_fieldset = (
            _("Contrôles de contenu"), {
                'fields': (
                    'display_resume', 'display_details', 'display_tags',
                    'display_author', 'display_author_skills',
                    'display_social_media', 'display_share_buttons'
                ),
                'classes': ('collapse',)
            }
        )
        
        # Construction des fieldsets selon le type
        fieldsets = [common_fieldset, image_fieldset, publication_fieldset]
        
        # Ajouter les champs spécifiques au type
        content_type = None
        if obj:
            content_type = obj.content_type
        elif 'content_type' in request.GET:
            content_type = request.GET['content_type']
        
        if content_type == 'project':
            fieldsets.insert(2, project_fieldset)
        elif content_type == 'service':
            fieldsets.insert(2, service_fieldset)
        
        fieldsets.extend([author_fieldset, controls_fieldset])
        
        return fieldsets
    
    def content_type_badge(self, obj):
        """Affiche le type de contenu avec couleur"""
        color_map = {
            'project': '#2c5282',
            'blog': '#4a90a4',
            'service': '#744210'
        }
        label_map = {
            'project': 'Projet',
            'blog': 'Article',
            'service': 'Service'
        }
        color = color_map.get(obj.content_type, '#666')
        label = label_map.get(obj.content_type, obj.content_type)
        
        return f'<span style="background-color: {color}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px; font-weight: bold;">{label}</span>'
    content_type_badge.short_description = _("Type")
    content_type_badge.allow_tags = True
    
    def save_model(self, request, obj, form, change):
        """Sauvegarde et log les modifications"""
        super().save_model(request, obj, form, change)
    
    class Meta:
        model = Content

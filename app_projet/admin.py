from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'is_published', 'author_name', 'published_at', 'updated_at')
    list_filter = ('featured', 'is_published', 'published_at')
    list_editable = ('featured', 'is_published')
    search_fields = ('title', 'resume', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)

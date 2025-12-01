from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'is_published', 'author_name', 'author_profession', 'published_at', 'updated_at')
    list_filter = ('featured', 'is_published', 'published_at')
    list_editable = ('featured', 'is_published')
    search_fields = ('title', 'resume', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)

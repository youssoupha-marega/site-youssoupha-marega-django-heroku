from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'is_published', 'created_at')
    list_filter = ('featured', 'is_published', 'created_at')
    list_editable = ('featured', 'is_published')
    search_fields = ('title', 'resume', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('created_at',)

from django.shortcuts import render, get_object_or_404
from .models import BlogPost

def blogue_list(request):
    """Liste de tous les articles de blog"""
    articles = BlogPost.objects.filter(is_published=True)
    return render(request, 'app_blog/list.html', {'articles': articles})

def blogue_detail(request, slug):
    """Détail d'un article de blog"""
    article = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'app_blog/detail.html', {'article': article})

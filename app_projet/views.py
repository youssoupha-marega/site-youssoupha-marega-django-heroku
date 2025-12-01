from django.shortcuts import render, get_object_or_404
from .models import Project

def projet_list(request):
    """Liste de tous les projets"""
    projets = Project.objects.filter(is_published=True)
    return render(request, 'app_projet/list.html', {'projets': projets})

def projet_detail(request, slug):
    """Détail d'un projet"""
    projet = get_object_or_404(Project, slug=slug)
    return render(request, 'app_projet/detail.html', {'projet': projet})

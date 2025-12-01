from django.shortcuts import render, get_object_or_404
from .models import Service

def service_list(request):
    """Liste de tous les services"""
    services = Service.objects.filter(is_published=True)
    return render(request, 'app_service/list.html', {'services': services})

def service_detail(request, slug):
    """Détail d'un service"""
    service = get_object_or_404(Service, slug=slug, is_published=True)
    return render(request, 'app_service/detail.html', {'service': service})

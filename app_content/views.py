from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from .models import Content


class ContentListView(ListView):
    """
    Affiche la liste du contenu filtré par type.
    URLs: /projets/, /blog/, /services/
    Supporte aussi les paramètres de profil dans l'URL
    """
    model = Content
    paginate_by = 12
    context_object_name = 'contents'
    template_name = 'app_content/content_list.html'
    
    def get_queryset(self):
        """Filtre par type de contenu"""
        content_type = self.kwargs.get('content_type')
        queryset = Content.objects.filter(
            content_type=content_type
        )
        
        # Tri par date décroissante
        queryset = queryset.order_by('-created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Ajoute les infos du type de contenu au contexte"""
        context = super().get_context_data(**kwargs)
        content_type = self.kwargs.get('content_type')
        
        # Info d'affichage pour le type
        type_labels = {
            'project': {'label': _('Projets'), 'icon': 'fa-rocket'},
            'blog': {'label': _('Articles'), 'icon': 'fa-pen-fancy'},
            'service': {'label': _('Services'), 'icon': 'fa-tools'},
        }
        
        context['type_info'] = type_labels.get(content_type, {})
        context['content_type'] = content_type
        
        # Ajouter info de profil si présente
        if 'nom' in self.kwargs:
            context['profile_nom'] = self.kwargs.get('nom')
        if 'profession' in self.kwargs:
            context['profile_profession'] = self.kwargs.get('profession')
        
        return context


class ContentDetailView(DetailView):
    """
    Affiche le détail d'un contenu spécifique.
    URL: /projets/<slug>/, /blog/<slug>/, /services/<slug>/
    Supporte aussi les paramètres de profil dans l'URL
    """
    model = Content
    context_object_name = 'content'
    template_name = 'app_content/content_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        """Filtre par type de contenu (depuis l'URL)"""
        content_type = self.kwargs.get('content_type')
        return Content.objects.filter(content_type=content_type)
    
    def get_context_data(self, **kwargs):
        """Ajoute les infos de type et contenus similaires"""
        context = super().get_context_data(**kwargs)
        content = self.object
        content_type = self.kwargs.get('content_type')
        
        # Infos d'affichage du type
        type_config = content.get_type_display_info()
        context['type_info'] = type_config
        context['content_type'] = content_type
        
        # Contenus similaires (3 autres du même type)
        context['related_contents'] = Content.objects.filter(
            content_type=content_type
        ).exclude(id=content.id)[:3]
        
        # Ajouter info de profil si présente
        if 'nom' in self.kwargs:
            context['profile_nom'] = self.kwargs.get('nom')
        if 'profession' in self.kwargs:
            context['profile_profession'] = self.kwargs.get('profession')
        
        return context


def search_content(request):
    """
    Recherche dans tous les contenus.
    Filtre par titre, résumé et contenu.
    """
    query = request.GET.get('q', '').strip()
    results = Content.objects.none()
    
    if query:
        results = Content.objects.filter(
            Q(title__icontains=query) |
            Q(resume__icontains=query) |
            Q(content__icontains=query)
        ).order_by('-created_at')
    
    context = {
        'query': query,
        'results': results,
        'count': results.count()
    }
    
    return render(request, 'app_content/search_results.html', context)

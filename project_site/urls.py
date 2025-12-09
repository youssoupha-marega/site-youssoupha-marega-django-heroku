"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from app_content import views as content_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URLs pour le profil par défaut (à la racine)
    path('', include('app_acceuil.urls')),
    path('', include('app_content.urls')),  # Unified content app
    
    # URLs pour les profils spécifiques avec paramètres dans le chemin
    # Format: /profil/nom=youssoupha-marega&profession=scientifique-de-donnees/projets/
    # Using unified app_content routes
    re_path(r'^profil/nom=(?P<nom>[^&/]+)&profession=(?P<profession>[^/]+)/projets/$', 
            content_views.ContentListView.as_view(), {'content_type': 'project'}, 
            name='profile_projet_list'),
    re_path(r'^profil/nom=(?P<nom>[^&/]+)&profession=(?P<profession>[^/]+)/projets/(?P<slug>[\w-]+)/$', 
            content_views.ContentDetailView.as_view(), {'content_type': 'project'}, 
            name='profile_projet_detail'),
    re_path(r'^profil/nom=(?P<nom>[^&/]+)&profession=(?P<profession>[^/]+)/blog/$', 
            content_views.ContentListView.as_view(), {'content_type': 'blog'}, 
            name='profile_blogue_list'),
    re_path(r'^profil/nom=(?P<nom>[^&/]+)&profession=(?P<profession>[^/]+)/blog/(?P<slug>[\w-]+)/$', 
            content_views.ContentDetailView.as_view(), {'content_type': 'blog'}, 
            name='profile_blogue_detail'),
    re_path(r'^profil/nom=(?P<nom>[^&/]+)&profession=(?P<profession>[^/]+)/services/$', 
            content_views.ContentListView.as_view(), {'content_type': 'service'}, 
            name='profile_service_list'),
    re_path(r'^profil/nom=(?P<nom>[^&/]+)&profession=(?P<profession>[^/]+)/services/(?P<slug>[\w-]+)/$', 
            content_views.ContentDetailView.as_view(), {'content_type': 'service'}, 
            name='profile_service_detail'),
    
    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

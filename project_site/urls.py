
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
from app_projet import views as projet_views
from app_blog import views as blog_views
from app_service import views as service_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URLs pour le profil par défaut (à la racine)
    path('', include('app_acceuil.urls')),
    path('blogue/', include('app_blog.urls')),
    path('projets/', include('app_projet.urls')),
    path('services/', include('app_service.urls')),
    
    # URLs pour les profils spécifiques avec paramètres dans le chemin
    # Format: /profil/nom=youssoupha-marega&profession=scientifique-de-donnees/projets/
    re_path(r'^profil/nom=(?P<nom>[^&/]+)&profession=(?P<profession>[^/]+)/projets/$', projet_views.projet_list, name='profile_projet_list'),
    re_path(r'^profil/nom=(?P<nom>[^&/]+)&profession=(?P<profession>[^/]+)/projets/(?P<slug>[\w-]+)/$', projet_views.projet_detail, name='profile_projet_detail'),
    re_path(r'^profil/nom=(?P<nom>[^&/]+)&profession=(?P<profession>[^/]+)/blog/$', blog_views.blogue_list, name='profile_blogue_list'),
    re_path(r'^profil/nom=(?P<nom>[^&/]+)&profession=(?P<profession>[^/]+)/blog/(?P<slug>[\w-]+)/$', blog_views.blogue_detail, name='profile_blogue_detail'),
    re_path(r'^profil/nom=(?P<nom>[^&/]+)&profession=(?P<profession>[^/]+)/services/$', service_views.service_list, name='profile_service_list'),
    re_path(r'^profil/nom=(?P<nom>[^&/]+)&profession=(?P<profession>[^/]+)/services/(?P<slug>[\w-]+)/$', service_views.service_detail, name='profile_service_detail'),
    
    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

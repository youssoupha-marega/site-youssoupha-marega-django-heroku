from django.urls import path, re_path

from . import views

urlpatterns = [
    # Profil par défaut à la racine
    path('', views.acceuil, name='acceuil'),
    
    # Profil spécifique avec paramètres dans le chemin: /profil/nom=...&profession=.../
    re_path(r'^profil/nom=(?P<nom>[^&/]+)&profession=(?P<profession>[^/]+)/$', views.profile_home, name='profile_home'),
    
    # Contact
    path('contact/', views.contact, name='contact'),
]

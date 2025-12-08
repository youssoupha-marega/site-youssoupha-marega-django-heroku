from django.urls import path
from . import views

urlpatterns = [
    # URLs pour le profil par défaut
    path('', views.projet_list, name='projet_list'),
    path('<slug:slug>/', views.projet_detail, name='projet_detail'),
]

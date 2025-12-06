from django.urls import path
from . import views

urlpatterns = [
    # URLs pour le profil par défaut
    path('', views.blogue_list, name='blogue_list'),
    path('<slug:slug>/', views.blogue_detail, name='blogue_detail'),
]

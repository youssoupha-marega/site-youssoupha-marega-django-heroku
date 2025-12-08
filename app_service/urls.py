from django.urls import path
from . import views

urlpatterns = [
    # URLs pour le profil par défaut
    path('', views.service_list, name='service_list'),
    path('<slug:slug>/', views.service_detail, name='service_detail'),
]

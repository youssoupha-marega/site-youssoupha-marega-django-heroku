from django.urls import path

from . import views

#from .views import home

#urlpatterns = [
#    path('', home, name='home'),
#]


urlpatterns = [
    path('', views.acceuil, name='acceuil'),
    path('contact/', views.contact, name='contact'),
]

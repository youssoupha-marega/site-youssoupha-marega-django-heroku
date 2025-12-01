from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogue_list, name='blogue_list'),
    path('<slug:slug>/', views.blogue_detail, name='blogue_detail'),
]

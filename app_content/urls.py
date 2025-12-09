from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    # Liste par type
    path('projets/', views.ContentListView.as_view(), {'content_type': 'project'}, name='projects_list'),
    path('blog/', views.ContentListView.as_view(), {'content_type': 'blog'}, name='blog_list'),
    path('services/', views.ContentListView.as_view(), {'content_type': 'service'}, name='services_list'),
    
    # Détail par type
    path('projets/<slug:slug>/', views.ContentDetailView.as_view(), {'content_type': 'project'}, name='project_detail'),
    path('blog/<slug:slug>/', views.ContentDetailView.as_view(), {'content_type': 'blog'}, name='blog_detail'),
    path('services/<slug:slug>/', views.ContentDetailView.as_view(), {'content_type': 'service'}, name='service_detail'),
    
    # Recherche générale
    path('search/', views.search_content, name='search'),
]

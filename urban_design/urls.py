from django.urls import path
from . import views

urlpatterns = [
    # Authentification
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Home and Dashboard
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Projets
    path('projets/', views.projet_list_view, name='projet_list'),
    path('projets/ajouter/', views.projet_create_view, name='projet_create'),
    path('projets/<int:pk>/', views.projet_detail_view, name='projet_detail'),
    path('projets/<int:pk>/modifier/', views.projet_update_view, name='projet_update'),
    path('projets/<int:pk>/supprimer/', views.projet_delete_view, name='projet_delete'),
    
    # Génération
    path('projets/<int:pk>/generer-proposition/', views.generer_proposition_view, name='generer_proposition'),
    path('projets/<int:pk>/generer-image-prompt/', views.generer_prompt_image_view, name='generer_prompt_image'),
]

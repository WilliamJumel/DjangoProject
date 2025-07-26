from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('membres/', views.membre_list, name='membre_list'),
    path('membres/ajouter/', views.membre_create, name='membre_create'),
    path('medias/', views.media_list, name='media_list'),
    path('emprunts/', views.emprunt_create, name='emprunt_create'),
    path('emprunts/retour/<int:pk>/', views.rendre_emprunt, name='rendre_emprunt'),
]

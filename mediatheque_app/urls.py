from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('membres/', views.membre_list, name='membre_list'),
    path('membres/ajouter/', views.membre_create, name='membre_create'),
    path('medias/', views.media_list, name='media_list'),
    path('medias/ajouter/', views.media_create, name='media_create'),
    path('emprunts/', views.emprunt_list, name='emprunt_list'),
    path('emprunts/ajouter/', views.emprunt_create, name='emprunt_create'),
    path('client/', views.client_home, name='client_home'),  # 👈 ligne ajoutée ici
]


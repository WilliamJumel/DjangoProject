from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mediatheque_app.urls')),  # 👈 on ajoute notre app ici
]

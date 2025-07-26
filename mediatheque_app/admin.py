from django.contrib import admin
from .models import Membre, Media, Emprunt, JeuDePlateau

admin.site.register(Membre)
admin.site.register(Media)
admin.site.register(Emprunt)
admin.site.register(JeuDePlateau)

# Register your models here.

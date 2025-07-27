from django import forms
from .models import Media, Membre, Emprunt

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['titre', 'type_media', 'auteur', 'disponible']

class MembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['nom', 'bloque']

class EmpruntForm(forms.ModelForm):
    class Meta:
        model = Emprunt
        fields = ['media', 'membre']
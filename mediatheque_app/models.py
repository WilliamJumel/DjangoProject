from django.db import models
from django.utils import timezone

class Membre(models.Model):
    nom = models.CharField(max_length=100)
    bloque = models.BooleanField(default=False)

    def __str__(self):
        return self.nom

class Media(models.Model):
    titre = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)
    date_emprunt = models.DateTimeField(null=True, blank=True)
    emprunteur = models.ForeignKey(Membre, null=True, blank=True, on_delete=models.SET_NULL)
    TYPE_CHOICES = [
        ('livre', 'Livre'),
        ('dvd', 'DVD'),
        ('cd', 'CD'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.titre} ({self.type})"

    def en_retard(self):
        if self.date_emprunt:
            return (timezone.now() - self.date_emprunt).days > 7
        return False

class JeuDePlateau(models.Model):
    titre = models.CharField(max_length=100)
    createur = models.CharField(max_length=100)

    def __str__(self):
        return self.titre

class Emprunt(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    date_emprunt = models.DateTimeField(default=timezone.now)
    rendu = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.media} emprunté par {self.membre}"
from django.db import models

# Create your models here.

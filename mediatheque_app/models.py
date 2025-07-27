from django.db import models
from django.utils import timezone
from datetime import timedelta

# Classe de base pour les médias
class Media(models.Model):
    nom = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)

    class Meta:
        abstract = True  # cette classe ne crée pas de table

    def __str__(self):
        return self.nom


class Livre(Media):
    auteur = models.CharField(max_length=100)
    date_emprunt = models.DateField(null=True, blank=True)
    emprunteur = models.ForeignKey("Membre", null=True, blank=True, on_delete=models.SET_NULL)


class Dvd(Media):
    realisateur = models.CharField(max_length=100)
    date_emprunt = models.DateField(null=True, blank=True)
    emprunteur = models.ForeignKey("Membre", null=True, blank=True, on_delete=models.SET_NULL)


class Cd(Media):
    artiste = models.CharField(max_length=100)
    date_emprunt = models.DateField(null=True, blank=True)
    emprunteur = models.ForeignKey("Membre", null=True, blank=True, on_delete=models.SET_NULL)


class JeuDePlateau(models.Model):
    nom = models.CharField(max_length=100)
    createur = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Membre(models.Model):
    nom = models.CharField(max_length=100)
    bloque = models.BooleanField(default=False)

    def __str__(self):
        return self.nom

    def emprunts_en_cours(self):
        return Emprunt.objects.filter(membre=self, rendu=False).count()

    def est_en_retard(self):
        emprunts = Emprunt.objects.filter(membre=self, rendu=False)
        for emprunt in emprunts:
            if emprunt.date_emprunt + timedelta(days=7) < timezone.now().date():
                return True
        return False


class Emprunt(models.Model):
    media_type = models.CharField(max_length=10, choices=[
        ('livre', 'Livre'),
        ('dvd', 'DVD'),
        ('cd', 'CD'),
    ])
    media_id = models.PositiveIntegerField()
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    date_emprunt = models.DateField(default=timezone.now)
    rendu = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.media_type} emprunté par {self.membre}"

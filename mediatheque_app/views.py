from django.shortcuts import render, redirect
from .models import Media, Membre, Emprunt
from .forms import MediaForm, MembreForm, EmpruntForm
from datetime import timedelta
from django.utils import timezone

def accueil_bibliothecaire(request):
    return render(request, 'bibliothecaire/accueil.html')

def ajouter_media(request):
    if request.method == 'POST':
        form = MediaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_medias')
    else:
        form = MediaForm()
    return render(request, 'bibliothecaire/ajouter_media.html', {'form': form})

def ajouter_membre(request):
    if request.method == 'POST':
        form = MembreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_membres')
    else:
        form = MembreForm()
    return render(request, 'bibliothecaire/ajouter_membre.html', {'form': form})

def liste_medias(request):
    medias = Media.objects.all()
    return render(request, 'bibliothecaire/liste_medias.html', {'medias': medias})

def liste_membres(request):
    membres = Membre.objects.all()
    return render(request, 'bibliothecaire/liste_membres.html', {'membres': membres})

def creer_emprunt(request):
    if request.method == 'POST':
        form = EmpruntForm(request.POST)
        if form.is_valid():
            emprunt = form.save(commit=False)
            media = emprunt.media
            membre = emprunt.membre

            # Vérifier si le média est empruntable
            if media.type_media == 'jeu':
                form.add_error(None, "Les jeux de plateau ne peuvent pas être empruntés.")
            elif not media.disponible:
                form.add_error(None, "Ce média est déjà emprunté.")
            elif membre.bloque or membre.emprunt_set.filter(date_retour__isnull=True).count() >= 3:
                form.add_error(None, "Ce membre ne peut pas emprunter de média.")
            else:
                media.disponible = False
                media.save()
                emprunt.date_emprunt = timezone.now()
                emprunt.save()
                return redirect('liste_emprunts')
    else:
        form = EmpruntForm()
    return render(request, 'bibliothecaire/creer_emprunt.html', {'form': form})

def liste_emprunts(request):
    emprunts = Emprunt.objects.all()
    return render(request, 'bibliothecaire/liste_emprunts.html', {'emprunts': emprunts})

def client_home(request):
    emprunts_actifs = Emprunt.objects.filter(retour__isnull=True).values_list('media_id', flat=True)
    medias_disponibles = Media.objects.exclude(id__in=emprunts_actifs)

    membre_id = request.GET.get('membre_id')
    emprunts = []
    membre_recherche = False

    if membre_id:
        membre_recherche = True
        emprunts = Emprunt.objects.filter(membre_id=membre_id)

    context = {
        'medias_disponibles': medias_disponibles,
        'emprunts': emprunts,
        'membre_recherche': membre_recherche
    }
    return render(request, 'mediatheque.app/client_home.html', context)


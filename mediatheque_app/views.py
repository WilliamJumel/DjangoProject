from django.shortcuts import render, redirect, get_object_or_404
from .models import Membre, Media, Emprunt
from django.utils import timezone

def home(request):
    return render(request, 'mediatheque_app/home.html')

def membre_list(request):
    membres = Membre.objects.all()
    return render(request, 'mediatheque_app/membre_list.html', {'membres': membres})

def membre_create(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        Membre.objects.create(nom=nom)
        return redirect('membre_list')
    return render(request, 'mediatheque_app/membre_create.html')

def media_list(request):
    medias = Media.objects.all()
    return render(request, 'mediatheque_app/media_list.html', {'medias': medias})

def emprunt_create(request):
    membres = Membre.objects.all()
    medias = Media.objects.filter(disponible=True)

    if request.method == 'POST':
        membre_id = request.POST.get('membre')
        media_id = request.POST.get('media')
        membre = Membre.objects.get(id=membre_id)
        media = Media.objects.get(id=media_id)

        # Contraintes métier
        emprunts = Emprunt.objects.filter(membre=membre, rendu=False)
        en_retard = any((timezone.now() - e.date_emprunt).days > 7 for e in emprunts)

        if emprunts.count() >= 3 or en_retard:
            return render(request, 'mediatheque_app/emprunt_erreur.html', {'membre': membre})

        Emprunt.objects.create(membre=membre, media=media)
        media.disponible = False
        media.emprunteur = membre
        media.date_emprunt = timezone.now()
        media.save()
        return redirect('media_list')

    return render(request, 'mediatheque_app/emprunt_create.html', {'membres': membres, 'medias': medias})

def rendre_emprunt(request, pk):
    emprunt = get_object_or_404(Emprunt, pk=pk)
    emprunt.rendu = True
    emprunt.save()
    media = emprunt.media
    media.disponible = True
    media.emprunteur = None
    media.date_emprunt = None
    media.save()
    return redirect('media_list')
from django.shortcuts import render

# Create your views here.

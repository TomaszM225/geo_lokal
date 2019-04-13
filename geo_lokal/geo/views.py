from django.shortcuts import render
from geo.models import Lokalizacja
from geo.forms import LokalizacjaForm



def index(request): #Widok strony głównej
    """Strona główna """

    context = {
        'ogloszenia_wszyscy':'lokalizacje'
    }
    return render(request, 'geo/index.html', context=context)

def nowa_lokalizacja(request):
    """Dodanie nowej loklalizacji"""
    if request.method == "POST":
        form = LokalizacjaForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            #Procedura sprawdzania wysokości nad poziomem moża
            form.save()
    else:
        form = LokalizacjaForm()
    return render(request, 'geo/nowa_lokalizacja.html', {'form': form})

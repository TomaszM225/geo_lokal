from django.shortcuts import render
from django.http import HttpResponse, JsonResponse #dla wyświtlania pliku PDF, JSON do przesyłania danych JSON 
from geo.models import Lokalizacja
from geo.forms import LokalizacjaForm
import requests
import json

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
            nazwa = request.POST.get('nazwa')
            szerokosc = request.POST.get('szerokosc')
            dlugosc = request.POST.get('dlugosc')
            url='https://elevation-api.io/api/elevation?points=('+szerokosc+','+dlugosc+')'
            wysokosc_dane = requests.get(url).json()
            data={
            'nazwa':nazwa,
            'szerokosc':szerokosc,
            'dlugosc':dlugosc,
            'wysokosc':str(wysokosc_dane['elevations'][0]['elevation'])
            }
            new_form=LokalizacjaForm(data)
            nowa_lokalizacja_lokalizacja= new_form.save(commit=False) #tworzy instancje lokalizcji z wysokością
            nowa_lokalizacja_lokalizacja.save() #zapisuje
    else:
        form = LokalizacjaForm()
    return render(request, 'geo/nowa_lokalizacja.html', {'form': form})

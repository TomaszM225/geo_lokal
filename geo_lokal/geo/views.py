from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.http import HttpResponse, JsonResponse 
import requests
from decimal import Decimal
from math import radians, cos, sin, asin, sqrt

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

def haversine(dlugosc1, szerokosc1, dlugosc2, szerokosc2):
    """Obliczanie dystansu pomiedzy punktami reguła Haversine"""
    # zmiana stopni dziesiętnych na kąt w radianach
    dlugosc1, szerokosc1, dlugosc2, szerokosc2 = map(radians, [dlugosc1, szerokosc1, dlugosc2, szerokosc2])
    # reguła Haversine`go
    d_dlugosc = dlugosc2 - dlugosc1 
    d_szerokosc = szerokosc2 - szerokosc1 
    a = sin(d_szerokosc/2)**2 + cos(szerokosc1) * cos(szerokosc2) * sin(d_dlugosc/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Promień ziemi w km, dla mil warość 3956
    return c * r

def zbior_lokalizacji(request):
    """obsługa zbioru lokalizacjiw okolicy """
    if request.method == 'POST':
        nazwa = request.POST.get('current_name')
        odleglosc = Decimal(request.POST.get('odleglosc'))
        szerokosc = Decimal(request.POST.get('szerokosc'))
        dlugosc = Decimal(request.POST.get('dlugosc'))
        promien = Decimal(odleglosc/111) #w odległosci 1 st tj 111km
        lokalizacje_w_okolicy = get_list_or_404(Lokalizacja, szerokosc__range = ((szerokosc-promien), (szerokosc+promien)), dlugosc__range = ((dlugosc-promien), (dlugosc+promien)))
        Lokalizacje_zbor = {}
        
        for lokalizacje_w_okolicy in lokalizacje_w_okolicy:
            dystans=haversine(lokalizacje_w_okolicy.szerokosc,lokalizacje_w_okolicy.dlugosc,szerokosc,dlugosc)
            lokal = {'nazwa':lokalizacje_w_okolicy.nazwa, 'szerokosc':lokalizacje_w_okolicy.szerokosc,'dlugosc':lokalizacje_w_okolicy.dlugosc,'odleglosc':str(round(dystans, 3))}
            Lokalizacje_zbor[str(lokalizacje_w_okolicy.pk)] = lokal

        data={
            'Lokalizacje_zbor':Lokalizacje_zbor
        }
        return JsonResponse(data, safe=False)
    else:
        return render(request,'geo/zbior_lokalizacji.html')

def najblizsza_lokalizacja(request):
    """wskazanie najbliższej lokalizacji sprawdza wszystkie """
    if request.method == 'POST':
        nazwa = request.POST.get('current_name')
        szerokosc = Decimal(request.POST.get('szerokosc'))
        dlugosc = Decimal(request.POST.get('dlugosc'))
        lokalizacje_w_okolicy = Lokalizacja.objects.all() #pobiera do porównania wszystkie lokalizacje, mozna zrobic ogranicznik
        Lokalizacje_zbor = {}
        dmax = 6371 #dystans początkowy obwód ziemi
        for lokalizacje_w_okolicy in lokalizacje_w_okolicy:
            dystans=haversine(lokalizacje_w_okolicy.szerokosc,lokalizacje_w_okolicy.dlugosc,szerokosc,dlugosc)
            lokal = {'nazwa':lokalizacje_w_okolicy.nazwa, 'szerokosc':lokalizacje_w_okolicy.szerokosc,'dlugosc':lokalizacje_w_okolicy.dlugosc,'odleglosc':str(round(dystans, 3))}
            if lokalizacje_w_okolicy.szerokosc!=szerokosc and lokalizacje_w_okolicy.dlugosc!=dlugosc:
                if dystans < dmax:
                    dmax = dystans
                    data = {
                        'najblizsza':lokal
                    }
        return JsonResponse(data, safe=False)
    else:
        return render(request,'geo/najblizsza_lokalizacja.html')

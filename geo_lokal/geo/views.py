from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.http import HttpResponse, JsonResponse #dla wyświtlania pliku PDF, JSON do przesyłania danych JSON 
from decimal import Decimal
import requests
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

def zbior_lokalizacji(request):
    """Szukanie lokalizacji w podanym promieniu"""
    if request.method == 'POST':
        your_name = request.POST.get('current_name')
        szerokosc = Decimal(request.POST.get('szerokosc'))
        dlugosc = Decimal(request.POST.get('dlugosc'))
        odleglosc = Decimal(request.POST.get('odleglosc'))
        promien = odleglosc/111 #przeliczenie sytansu na stopnie dziesiętne 1st = 111km
        lokalizacje_w_okolicy = get_list_or_404(Lokalizacja, szerokosc__range=((szerokosc-promien), (szerokosc+promien)))
        print(lokalizacje_w_okolicy)
        #obsługa liczenia odległosci serializowanie danych
        data={
        'dlugosc':dlugosc,
        'szerokosc':szerokosc,
        'promien':promien,
        }
        return JsonResponse(data, safe=False)
    else:
        return render(request, 'geo/zbior_lokalizacji.html')

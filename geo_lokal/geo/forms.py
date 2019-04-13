from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from geo.models import Lokalizacja

class LokalizacjaForm(ModelForm):
    """Formulaz dodawania lokalizacji"""

    class Meta:
        model = Lokalizacja
        widgets    = {'wysokosc': forms.HiddenInput()}
        
        labels = { #label przy polach nalezy usunąc help_text z modelu bo się równiez wyświtla
            "nazwa": "Nazwa lokalizcji",
            "szerokosc":"Szerokość geograficzna",
            "dlugosc":"Długośc geograficzna"
        }
        fields = ('nazwa','szerokosc','dlugosc','wysokosc')
        
        help_texts = { #zastępuje help_text z modelu na podany Nonie = nic :)
            "nazwa":"max 255 znaków",
            "szerokosc": "szerokość w stopniach dziesiętnych",
            "dlugosc": "długość w stopniach dziesiętnych"
        }



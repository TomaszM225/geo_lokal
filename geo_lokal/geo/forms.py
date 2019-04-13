from django.forms import ModelForm
from django.contrib.auth.models import User
from geo.models import Lokalizacja

class LokalizacjaForm(ModelForm):
    """Formulaz dodawania lokalizacji"""

    class Meta:
        model = Lokalizacja
        exclude = (
        'wysokosc',
        )
        labels = { #label przy polach nalezy usunąc help_text z modelu bo się równiez wyświtla
            "nazwa": "Nazwa lokalizcji",
            "szerokosc":"Szerokość geograficzna",
            "dlugosc":"Długośc geograficzna"
        }
        fields = ('nazwa','szerokosc','dlugosc')
        
        help_texts = { #zastępuje help_text z modelu na podany Nonie = nic :)
            "nazwa":"max 255 znaków",
            "szerokosc": "szerokość w stopniach dziesiętnych",
            "dlugosc": "długość w stopniach dziesiętnych"
        }



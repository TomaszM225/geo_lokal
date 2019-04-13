from django.db import models

# Create your models here.


class Lokalizacja(models.Model):
    """Znak przy wartości wsakzuje miejsce.
    Szerokość N wartość dodatnia, S wartość ujemna,
    długość E wartość dodatnia, W wartość ujemna"""
    nazwa =  models.CharField(max_length = 255, help_text = 'Nazwa lokalizacji')
    wysokosc = models.DecimalField(max_digits = 5, decimal_places = 1)
    szerokosc =  models.DecimalField( max_digits = 7, decimal_places = 5)
    dlugosc = models.DecimalField(max_digits = 7, decimal_places = 5)
    
    class Meta:
        db_table = 'n_lokalizacje'
        verbose_name_plural = "Lokalizacje"

    def __str__(self):
        nazwa = Lokalizacja.objects.get(pk=self.pk)
        return str(nazwa)

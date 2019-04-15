from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dodaj$', views.nowa_lokalizacja, name='nowa_lokalizacja'),
    url(r'^zbior$', views.zbior_lokalizacji, name='zbior_lokalizacji'),
    url(r'^najblizsza$', views.najblizsza_lokalizacja, name='najblizsza_lokalizacja'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('summoner/<str:region>/<str:name>', views.summoner, name='summoner')
]

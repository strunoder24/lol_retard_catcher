from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_accounts', views.add_account, name='add_account'),
    path('summoner/<str:region>/<str:name>', views.summoner, name='summoner')
]

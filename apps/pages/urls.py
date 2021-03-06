from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_accounts', views.add_account, name='add_account'),
    path('add_retard', views.add_retard, name='add_retard'),
    path('kill-profile', views.profile_destroy, name='profile_kill'),
    path('<str:account>', views.profile, name='profile'),
]

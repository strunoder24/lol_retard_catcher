from django.shortcuts import render, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate
import requests as ajax

from project.helpers.LeagueApiHelpers import LolApiHelperInstance


def index(request):
    user = request.user
    context = {}

    if hasattr(user, 'profile'):
        context['profiles'] = user.profile

    return render(request, 'pages/index.html')


def summoner(request, region, name):
    summoner = LolApiHelperInstance.summoner_formatter(username=name, region=region)
    pass


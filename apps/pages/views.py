from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import IntegrityError
import requests as ajax

from apps.accounts.models import Profile

from project.helpers.LeagueApiHelpers import LolApiHelperInstance


def index(request):
    user = request.user
    context = {}

    if user.is_authenticated:
        profiles = Profile.objects.order_by('-id').filter(user=user)
        paginator = Paginator(profiles, 10)
        page = request.GET.get('p')
        profile_page = paginator.get_page(page)

        context = {
            'profiles': profile_page
        }

    return render(request, 'pages/index.html', context)


def profile(request, profile):
    if request.user.is_authenticated:
        profile = Profile.objects.filter(name=profile, user=request.user)

        return render(request, 'pages/profile.html')

    return redirect('index')


def profile_destroy(request):
    if request.method == 'POST':
        name = request.POST['profile_name']
        Profile.objects.filter(name=name, user=request.user).delete()

    return redirect('index')


def add_account(request):
    if request.method == 'POST':
        username = request.POST['username']
        region = request.POST['region']

        lol_user = LolApiHelperInstance.get_summoner(username=username, region=region)

        if lol_user:
            try:
                Profile.objects.create(name=username, region=region, user=request.user,
                                       encrypted_id=lol_user['id'], level=lol_user['summonerLevel'],
                                       icon=LolApiHelperInstance.get_summoner_icon_url(summoner=lol_user))

            except IntegrityError:
                return JsonResponse({
                    'status': '400',
                    'message': 'Такой пользователь уже добавлен'
                }, status=400)

            messages.success(request, 'Пользователь успешно добавлен')
            return JsonResponse({
                'status': '200',
                'message': 'Пользователь успешно добавлен'
            }, status=200)

        else:
            return JsonResponse({
                'status': '400',
                'message': 'В данном регионе не существует указанного пользователя'
            }, status=400)


def summoner(request):
    pass

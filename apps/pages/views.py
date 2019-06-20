from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import requests as ajax

from apps.accounts.models import Profile
from apps.retards.models import Retard

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


def profile(request, account):
    lol_account = Profile.objects.get(name=account, user=request.user)

    if request.user.is_authenticated and lol_account:
        context = {
            'lol_account': lol_account
        }

        return render(request, 'pages/profile.html')
    else:
        return redirect('index')


def profile_destroy(request):
    if request.method == 'POST':
        name = request.POST['profile_name']
        Profile.objects.get(name=name, user=request.user).delete()

    return redirect('index')


def add_account(request):
    if request.method == 'POST':
        username = request.POST['username']
        region = request.POST['region']

        try:
            Profile.objects.get(name=username, user=request.user)
            return JsonResponse({
                'status_code': '400',
                'message': 'Такой пользователь уже добавлен'
            }, status=400)

        except ObjectDoesNotExist:  # Если объект не найден, то его надо добавить
            lol_user = LolApiHelperInstance.get_summoner(username=username, region=region)

            if 'status_code' not in lol_user or lol_user['status_code'] == 200:
                Profile.objects.create(name=username, region=region, user=request.user,
                                       encrypted_id=lol_user['id'], level=lol_user['summonerLevel'],
                                       icon=LolApiHelperInstance.get_summoner_icon_url(summoner=lol_user))
                messages.success(request, 'Пользователь успешно добавлен')
                return JsonResponse({
                    'status': '200',
                    'message': 'Пользователь успешно добавлен'
                }, status=200)

            elif lol_user['status_code'] == 403:
                return JsonResponse(lol_user, status=403)

            else:
                return JsonResponse({
                    'status_code': '400',
                    'message': 'В данном регионе не существует указанного пользователя'
                }, status=400)


def add_retard(request):
    if request.method == 'POST':
        username = request.POST['username']
        region = request.POST['region']
        description = request.POST['description']

        # lol_user = LolApiHelperInstance.get_summoner(username=username, region=region)
        #
        # if 'status_code' not in lol_user or lol_user['status_code'] == 200:  # Когда ответ успешен, поле status_code не приходит
        #     try:
        #         Retard.objects.create(name=username, region=region, user=request.user, description=description,
        #                               encrypted_id=lol_user['id'], level=lol_user['summonerLevel'],
        #                               icon=LolApiHelperInstance.get_summoner_icon_url(summoner=lol_user))
        #
        #     except IntegrityError:
        #         return JsonResponse({
        #             'status_code': '400',
        #             'message': 'Такой пользователь уже есть в чёрном списке'
        #         }, status=400)
        #
        #     messages.success(request, 'Пользователь успешно добавлен')
        #     return JsonResponse({
        #         'status': '200',
        #         'message': 'Пользователь успешно добавлен в чёрный список'
        #     }, status=200)
        #
        # elif lol_user['status_code'] == 403:
        #     return JsonResponse(lol_user, status=403)
        #
        # else:
        #     return JsonResponse({
        #         'status_code': '400',
        #         'message': 'В данном регионе не существует указанного пользователя'
        #     }, status=400)

from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from project.helpers.LeagueApiHelpers import LolApiHelperInstance


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        region = request.POST['region']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        summoner = LolApiHelperInstance.get_summoner(username=username, region=region)

        if password1 != password2:
            messages.error(request, 'Пароли не совпадают')

        elif summoner:
            try:
                user = get_user_model().objects.create_user(username=username, email=None, password=password1)
                user.profile.region = region
                user.profile.icon = LolApiHelperInstance.get_summoner_icon_url(summoner=summoner)
                user.profile.level = summoner['summonerLevel']
                user.profile.encrypted_id = summoner['id']
                user.save()
                messages.success(request, 'Вы успешно зарегистрировались')
                return redirect('login')

            except IntegrityError:
                messages.error(request, 'Такой пользователь уже зарегистрирован в сервисе')

        else:
            messages.error(request, 'Пользователя с таким именем в игре не существует')

        return render(request, 'accounts/register.html')

    elif request.method == 'GET':
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Вы авторизованны!')
            return redirect('index')
        else:
            messages.error(request, 'Имя пользователя и/или пароль введены неверно')
            return redirect('login')

    elif request.method == 'GET':
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Выход из аккаунты успешен!')
        return redirect('index')

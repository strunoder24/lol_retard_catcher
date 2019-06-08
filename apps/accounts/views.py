from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from project.variables import api_key

import requests as ajax


def is_exist(username, region):
    response = ajax.get(
        f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}?api_key={api_key}')
    if response.status_code == 200:
        return True

    return False


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        region = request.POST['region']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Пароли не совпадают')
            return redirect('register')

        elif is_exist(username=username, region=region):
            try:
                get_user_model().objects.create_user(username=username, email=None, password=password1)
                messages.success(request, 'Вы успешно зарегистрировались')
                return redirect('login')

            except IntegrityError:
                messages.error(request, 'Такой пользователь уже зарегистрирован в сервисе')

            return render(request, 'accounts/register.html')

        else:
            messages.error(request, 'Пользователя с таким именем в игре не существует')

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

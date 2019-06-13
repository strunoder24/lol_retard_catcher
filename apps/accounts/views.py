from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from project.helpers.LeagueApiHelpers import LolApiHelperInstance


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Пароли не совпадают')

        else:
            try:
                get_user_model().objects.create_user(username=username, email=None, password=password1)
                messages.success(request, 'Вы успешно зарегистрировались!\nТеперь используйте свои данные чтобы войти')
                return redirect('login')

            except IntegrityError:
                messages.error(request, 'Такой пользователь уже зарегистрирован в сервисе')

        return render(request, 'accounts/register.html')

    elif request.method == 'GET':
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = get_user_model().objects.filter(username=username)
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
        return redirect('index')

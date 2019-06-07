from django.shortcuts import render
from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate

import requests as ajax


def index(request):
    return render(request, 'pages/index.html')

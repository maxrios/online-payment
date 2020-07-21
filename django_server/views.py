from user.forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect


def user_check(request):
    if request.user.is_superuser:
        return render(request, 'home_admin.html', {})
    elif request.user.is_authenticated:
        return render(request, 'home_user.html', {})
    else:
        return render(request, 'home.html', {})

from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect

from profiles.forms import RegistrationForm, AuthorizationForm
from profiles.models import User


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if not User.objects.filter(username=form.cleaned_data['username']).exists():
                user = User.objects.create_user(username=form.cleaned_data['username'])
                user.set_password(form.cleaned_data['password'])
                user.save()
                login(request, user)
                return redirect('profile', user_id=user.id)
            form.add_error(None, 'Пользователь с таким username существует')
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'profiles/registration.html', context)

def authorization(request):
    if request.method == 'POST':
        form = AuthorizationForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('profile', user_id=user.id)
            form.add_error(None, 'Неверный логин или пароль')

    else:
        form = AuthorizationForm()

    context = {'form': form}
    return render(request, 'profiles/authorization.html', context)

def profile(request, user_id):
    return HttpResponse(str(user_id))
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from profiles.forms import RegistrationForm, AuthorizationForm, EditForm
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
    profile_user = get_object_or_404(User, id=user_id)

    context = {'profile_user': profile_user}
    return render(request, 'profiles/profile.html', context)


@login_required()
def edit(request):
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.information = form.cleaned_data['information']
            user.save()
            return redirect('profile', user_id=user.id)
    else:
        form = EditForm()
    context = {'form': form}
    return render(request, 'profiles/edit.html', context)

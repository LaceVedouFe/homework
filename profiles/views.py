from django.contrib.auth import login
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect

from profiles.forms import RegistrationForm
from profiles.models import User


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                raise ValidationError('Пользователь с таким username существует')
            user = User.objects.create_user(username=form.cleaned_data['username'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('profile', user_id=user.id)

    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'profiles/registration.html', context)

def profile(request, user_id):
    return HttpResponse(str(user_id))
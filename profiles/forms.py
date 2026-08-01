from django import forms
from django.core.exceptions import ValidationError


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Ваше имя', min_length=4, max_length=30)
    password = forms.CharField(label='Пароль', min_length=8, max_length=20, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label='Подтверждение пароля', min_length=8, max_length=20, widget=forms.PasswordInput)

    def clean(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            raise ValidationError('Пароли не совпадают')
        return self.cleaned_data

class AuthorizationForm(forms.Form):
    username = forms.CharField(label='Ваше имя', min_length=4, max_length=30)
    password = forms.CharField(label='Пароль', min_length=8, max_length=20, widget=forms.PasswordInput)

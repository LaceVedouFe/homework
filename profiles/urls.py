from django.urls import path

from profiles.views import registration, profile

urlpatterns = [
    path('registration/', registration, name='registration'),
    path('<int:user_id>', profile, name='profile'),
]
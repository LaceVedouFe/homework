from django.urls import path

from profiles.views import registration, profile, authorization

urlpatterns = [
    path('registration/', registration, name='registration'),
    path('<int:user_id>', profile, name='profile'),
    path('authorization/', authorization, name='authorization'),
]
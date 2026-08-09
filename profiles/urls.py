from django.urls import path

from profiles.views import registration, profile, authorization, edit

urlpatterns = [
    path('registration/', registration, name='registration'),
    path('<int:user_id>/', profile, name='profile'),
    path('authorization/', authorization, name='authorization'),
    path('edit/', edit, name='edit'),
]
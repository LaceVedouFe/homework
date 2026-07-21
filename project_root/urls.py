from django.contrib import admin
from django.urls import path, re_path

from common_utils.views import feature_flags, change_feature_flag_status

urlpatterns = [
    path('admin/feature-flags/', feature_flags, name='feature_flags'),
    path('admin/feature-flags/change-status/', change_feature_flag_status, name='change_feature_flag_status'),
    path('admin/', admin.site.urls),
]

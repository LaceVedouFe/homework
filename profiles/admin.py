from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from profiles.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Админ-модель: Учетная запись пользователя"""
    list_display = ('id', 'email', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

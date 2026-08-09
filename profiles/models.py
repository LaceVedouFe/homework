from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель: Пользователь"""

    class Meta:
        """Класс метаданных"""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'Пользователь#{self.id}'

    def save(self, *args, **kwargs):
        """Метод сохранения модели"""
        if self.email:
            self.email = self.email.lower()

        super().save(*args, **kwargs)

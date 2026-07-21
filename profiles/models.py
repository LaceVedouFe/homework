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


class Team(models.Model):
    """Модель: Команда"""

    hltv_id = models.IntegerField(verbose_name='Идентификатор на HLTV')
    hltv_link = models.URLField(verbose_name='Ссылка на HLTV')

    class Meta:
        """Класс метаданных"""

        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    def __str__(self):
        return f'Команда#{self.id}'

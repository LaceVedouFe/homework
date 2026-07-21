import os
import types
from datetime import timedelta
from functools import singledispatch, wraps
from inspect import getfile
from pathlib import Path
from typing import Type, Union

from celery import Celery, Task
from celery.schedules import crontab
from django.conf import settings
from django.core.management import BaseCommand, call_command
from kombu import Queue

from common_utils.constants import QueueName


class _Celery(Celery):
    """Главный класс Celery"""

    class _WithTask:
        task: Task

    def scheduled(
        self,
        schedule: Union[crontab, timedelta, int],
        *args,
        **kwargs,
    ):
        """Добавляет task в расписание

        Использовать выше декоратора @task

        Возможно использование нескольких декораторов подряд, но во время вызова экземпляр задачи будет одинаковым
        @scheduled(60)
        @scheduled(crontab(), some_arg=123)
        @task
        def ...

        :param schedule: Периодичность запуска задачи.
        :param args: Позиционные аргументы, которые будут переданы в таск при запуске.
        :param kwargs: Именованные аргументы, которые будут переданы в таск при запуске.
        """
        if isinstance(schedule, crontab) and schedule._orig_hour != '*' and schedule._orig_minute == '*':
            raise ValueError(
                f'Task will run every minute between {schedule._orig_hour}:00 and {schedule._orig_hour}:59. '
                'Are you sure about this? If not, enter 0 minutes. Else enter list(range(60)) in minutes.',
            )

        def _scheduled(obj):
            if isinstance(obj, type) and issubclass(obj, self._WithTask):
                task = obj.task
            else:
                task = obj

            beat_key = f'{task.name}:{str(schedule)}'
            if beat_key in self.conf.beat_schedule:
                raise KeyError('Attempt to override an existing task in the schedule')

            self.conf.beat_schedule[beat_key] = {
                'task': task.name,
                'schedule': schedule,
                'args': args,
                'kwargs': kwargs,
            }

            return obj

        return _scheduled

    def autodiscover_django_commands(self):
        """Обрабатывает django команды с целью сделать из них задачи"""
        commands = [
            str(command_path.with_suffix('')).replace('/', '.')
            for command_path in Path().glob('*/management/commands/*.py')
            if not command_path.stem.startswith('_')
        ]

        self.autodiscover_tasks(commands, related_name=None)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_root.settings')

app = _Celery('homework')
app.conf.update(
    broker_url=settings.CELERY_BROKER_URL,
    task_time_limit=settings.CELERY_TASK_TIME_LIMIT,
    result_expires=settings.CELERY_RESULT_EXPIRES,
    timezone=settings.CELERY_TIMEZONE,
    enable_utc=settings.CELERY_ENABLE_UTC,
)

app.autodiscover_tasks()
app.autodiscover_django_commands()

app.conf.task_default_queue = "default"
app.conf.task_queues = (
    Queue(QueueName.DEFAULT),
    Queue(QueueName.HIGH_PRIORITY),
)

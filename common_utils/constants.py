class FeatureFlagStatus:
    """Перечисление названий статусов Feature флагов"""

    DISABLED = 'disabled'
    ALL = 'all'
    IP = 'ip'


class QueueName:
    """Перечисление названий очередей Celery"""

    DEFAULT = 'default'
    HIGH_PRIORITY = 'high_priority'

from typing import Final

from django.conf import settings
from django.http import HttpRequest

from common_utils.constants import FeatureFlagStatus
from common_utils.redis.connection import redis_connection
from common_utils.redis.keys import FEATURE_FLAGS

SERVER_FEATURE_FLAGS: Final[dict[str, str]] = {
}


def is_feature_enabled(request: HttpRequest | None, flag_name: str) -> bool:
    if flag_name not in SERVER_FEATURE_FLAGS:
        raise ValueError(f'Проверяется несуществующий feature флаг: {flag_name}')

    r_con = redis_connection()
    value = r_con.hget(FEATURE_FLAGS, flag_name) or False

    if not value:
        return False

    if value == FeatureFlagStatus.IP:
        if request is None:
            return False

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip in settings.TEST_IPS

    return True

from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from common_utils.constants import FeatureFlagStatus
from common_utils.decorators import has_group
from common_utils.feature_flags import SERVER_FEATURE_FLAGS
from common_utils.redis.connection import redis_connection
from common_utils.redis.keys import FEATURE_FLAGS


@login_required
@has_group('feature_flags')
def feature_flags(request: HttpRequest) -> HttpResponse:
    r_con = redis_connection()

    active_flags = r_con.hgetall(FEATURE_FLAGS)

    all_feature_flags: dict[str: str] = [
        {
            'name': name,
            'description': description,
            'status': active_flags.get(name, 'disabled'),
        }
        for name, description in SERVER_FEATURE_FLAGS.items()
    ]

    return render(request, 'admin/feature_flags.html', {'feature_flags': all_feature_flags})


def change_feature_flag_status(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        flag_name = request.POST.get('flag_name')
        new_status = request.POST.get('status')

        r_con = redis_connection()

        if new_status in [FeatureFlagStatus.IP, FeatureFlagStatus.ALL]:
            r_con.hset(FEATURE_FLAGS, flag_name, new_status)
        elif new_status == FeatureFlagStatus.DISABLED:
            r_con.hdel(FEATURE_FLAGS, flag_name)

    return redirect('feature_flags')

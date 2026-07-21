from django.contrib.auth.decorators import user_passes_test


def has_group(group_name):
    return user_passes_test(
        lambda u: u.is_superuser or u.groups.filter(name=group_name).exists()
    )

from django.conf import settings


def get_user_led_bounds(user_id):
    # user count starts from 1
    # led count for each user starts from 0
    lower_bound = (username_number - 1) * settings.LEDS_PER_USER
    upper_bound = lower_bound + settings.LEDS_PER_USER - 1

    return lower_bound, upper_bound

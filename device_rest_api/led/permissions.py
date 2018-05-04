from rest_framework import permissions

from device_client import DeviceController


class AllowedOnLed(permissions.BasePermission):

    def has_permission(self, request, view):
        # we take for granted that the user is something like "blabla-\d+"
        username_number = int(request.user.username.split('-')[-1])

        lower_bound = (username_number - 1) * 10
        upper_bound = (username_number - 1) * 10 + 9

        led_number = int(view.kwargs['led_number'])
        if led_number < lower_bound or led_number > upper_bound:
            with DeviceController(request.user.username) as ctl:
                # flash red
                ctl.send('led', '{}|{},255,0,0'.format(lower_bound, upper_bound))

            return False

        return True

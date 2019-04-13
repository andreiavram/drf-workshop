import time
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.permissions import IsAuthenticated

from device_client import DeviceController

from led.serializers import LEDRGBSerializer
from led.permissions import AllowedOnLed
from led.utils import get_user_led_bounds


class LedOpAPIView(generics.UpdateAPIView):

    serializer_class = LEDRGBSerializer
    permission_classes = (IsAuthenticated, AllowedOnLed)

    def get_object(self):
        # we don't need no object
        return

    def update(self, request, *args, **kwargs):
        """
        CURL EXAMPLE:
        curl -X PUT 'username-<id>:password@localhost:8000/device/led/3' -d '{"red": 10, "blue": 10, "green": 240}' -H 'Content-Type:application/json'
        When the request is wrong, all the LEDs of the user get lit.
        When the user requests some other LED which is not his/hers, all the LEDs
        get red.
        """
        try:
            return super(LedOpAPIView, self).update(self.request, *args, **kwargs)
        except ValidationError:
            username_number = int(self.request.user.username.split('-')[-1])

            lower_bound, upper_bound = get_user_led_bounds(username_number)
            # flash orange
            payload = '{}|{},255,0,128'.format(lower_bound, upper_bound)

            with DeviceController(self.request.user.username) as ctl:
                ctl.send('led', payload)

            raise

    def perform_update(self, serializer):
        with DeviceController(self.request.user.username) as ctl:
            payload = '{led},{red},{green},{blue}'.format(
                led=self.kwargs['led_number'], **serializer.validated_data)

            ctl.send('led', payload)


class MotorOpAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def put(self, request):
        """
        curl -X PUT 'username-<id>:password@localhost:8000/device/motor/'  -H 'Content-Type:application/json'
        """
        with DeviceController(self.request.user.username) as ctl:
            ctl.send('motor', '')
            for i in range(1, 10):
                ctl.send('led', 'all,0,0,0')
                time.sleep(0.5)
                ctl.send('led', '0|49,0,255,0')
                ctl.send('led', '50|99,255,0,211')
                ctl.send('led', '100|149,255,0,0')
                time.sleep(1)

        return Response({'action': 'ok'})

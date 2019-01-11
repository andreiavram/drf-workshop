from django.conf.urls import url, include
from django.contrib import admin


from led.views import LedOpAPIView, MotorOpAPIView


urlpatterns = [
    url(r'^led/(?P<led_number>\d+)', LedOpAPIView.as_view()),\
    url(r'^motor/', MotorOpAPIView.as_view()),
]

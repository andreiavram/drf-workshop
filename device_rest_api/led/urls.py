from django.conf.urls import url, include
from django.contrib import admin


from led.views import LedOpAPIView


urlpatterns = [
    url(r'^(?P<led_number>\d+)', LedOpAPIView.as_view()),
]

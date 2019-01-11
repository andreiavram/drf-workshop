from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.authtoken import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth-token', views.obtain_auth_token),
    url(r'^device/', include('led.urls')),
]

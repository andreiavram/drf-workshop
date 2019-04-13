from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'manager/', include('manager.urls')),
    path(r'rest-auth/', views.obtain_auth_token)
]

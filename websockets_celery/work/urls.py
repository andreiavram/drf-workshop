
from django.contrib import admin
from django.urls import path, include

from work.views import work_page, average_color


urlpatterns = [
    path('average-color/', average_color),
    path('<slug:name>/', work_page),
]

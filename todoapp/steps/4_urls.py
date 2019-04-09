# We use the function `path` to tell Django how we want our URLs to look like
from django.urls import path

# The views are here because we map each URL to a view we have created
from manager import views


# Django will look for a variable called `urlpatterns` and load the URLs
# defined in it
urlpatterns = [
    path('task/', views.list_tasks),
    path('board/<int:pk>/', views.get_board)
]

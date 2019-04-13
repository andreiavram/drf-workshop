# We use the function `path` to tell Django how we want our URLs to look like
from django.urls import path

# The views are here because we map each URL to a view we have created
from manager import views


# Django will look for a variable called `urlpatterns` and load the URLs
# defined in it
urlpatterns = [
    path('task/', views.TaskListCreateAPIView.as_view()),
    path('task/<int:pk>/', views.TaskRetrieveUpdateDestroyAPIView.as_view()),
    path('board/', views.BoardListCreateAPIView.as_view()),
    path('board/<int:pk>/', views.TaskRetrieveUpdateDestroyAPIView.as_view()),
    path('label/', views.LabelListCreateAPIView.as_view()),
    path('label/<int:pk>/', views.LabelRetrieveUpdateDestroyAPIView.as_view()),
]

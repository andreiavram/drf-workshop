# Django Rest Framework
from rest_framework import generics

from manager.models import Task, TaskBoard, Label
from manager.serializers import (
    TaskSerializer, TaskBoardSerializer, LabelSerializer)


# Because the URLs differ for listing/creating objects from the URLs
# used to retrieve/update/destroy an object, we use two different views for
# the two use cases
class TaskListCreateAPIView(generics.ListCreateAPIView):

    # We tell the view what model to use to fetch the data from the database
    queryset = Task.objects.all()

    # We also let it know what serializer should it use when
    # serializing/deserializing the objects
    serializer_class = TaskSerializer


class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class BoardListCreateAPIView(generics.ListCreateAPIView):

    queryset = TaskBoard.objects.all()
    serializer_class = TaskBoardSerializer


class BoardRetrieveUpdateDestropyAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = TaskBoard.objects.all()
    serializer_class = TaskBoardSerializer


class LabelListCreateAPIView(generics.ListCreateAPIView):

    queryset = Label.objects.all()
    serializer_class = LabelSerializer


class LabelRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Label.objects.all()
    serializer_class = LabelSerializer

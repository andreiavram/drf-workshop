from rest_framework import viewsets

from manager.serializers import TaskSerializer
from manager.models import Task


# Instead of having two views for working with Tasks, we can have only one, a
# smart one
# This view can deal with all the responsibilities of the prior two views, combined
class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSerializer
    queryset = Task.objects.all()

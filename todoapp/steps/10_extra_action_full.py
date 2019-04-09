from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from manager.serializers import TaskSerializer, TaskBoardSerializer, LabelSerializer
from manager.models import Task, TaskBoard, Label
from manager.constants import TaskState


# Instead of having two views for working with Tasks, we can have only one, a
# smart one
# This view can deal with all the responsibilities of the prior two views, combined
class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    @action(detail=False, methods=['GET'])
    def done_tasks(self, request):
        queryset = self.get_queryset().filter(state=TaskState.DONE)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class TaskBoardViewSet(viewsets.ModelViewSet):

    serializer_class = TaskBoardSerializer
    queryset = TaskBoard.objects.all()


class LabelViewSet(viewsets.ModelViewSet):

    serializer_class = LabelSerializer
    queryset = Label.objects.all()

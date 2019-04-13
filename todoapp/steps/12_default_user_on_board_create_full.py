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

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user, state=TaskState.DONE)

    @action(detail=False)
    def done_tasks(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class TaskBoardViewSet(viewsets.ModelViewSet):

    serializer_class = TaskBoardSerializer
    queryset = TaskBoard.objects.all()

    def get_serializer(self, *args, **kwargs):
        data = kwargs.get('data')
        if data is not None:
            data['user'] = self.request.user

        return super().get_serializer(*args, **kwargs)


class LabelViewSet(viewsets.ModelViewSet):

    serializer_class = LabelSerializer
    queryset = Label.objects.all()

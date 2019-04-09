from rest_framework.serializers import ModelSerializer

from manager.models import Task, TaskBoard, Label


# We set the model class on the serializer. This helps the serialize figure out
# how it should represent the data, e.g. dates, numbers or strings.
# It also gets a handle for creating objects in the database.
class TaskSerializer(ModelSerializer):

    class Meta:
        model = Task
        ## we choose all fields
        fields = '__all__'


class TaskBoardSerializer(ModelSerializer):

    class Meta:
        model = TaskBoard
        fields = '__all__'


class LabelSerializer(ModelSerializer):

    class Meta:
        model = Label
        fields = '__all__'

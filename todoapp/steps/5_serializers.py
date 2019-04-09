from rest_framework.serializers import ModelSerializer

from manager.models import Task


# We set the model class on the serializer. This helps the serialize figure out
# how it should represent the data, e.g. dates, numbers or strings.
# It also gets a handle for creating objects in the database.
class TaskSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = ['name', 'description']

# Lets use this serializer in our views to simplify how we create the response
# for the user

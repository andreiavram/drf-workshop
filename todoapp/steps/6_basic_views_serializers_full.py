import json
from datetime import date

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from manager.models import Task, TaskBoard
from manager.serializers import TaskSerializer, TaskBoardSerializer, LabelSerializer


@csrf_exempt
def list_tasks(request):
    """Return a JsonResponse with all Task records in the database"""
    # We list the Tasks only if the HTTP method is GET
    # What do we do when a POST comes in?
    if request.method == 'GET':
        # create a queryset for all the records from the Task model
        tasks = Task.objects.all()
        dict_tasks = TaskSerializer(tasks, many=True).data

        # return a JSON response (sets content type to "application/json")
        return JsonResponse(dict_tasks, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        serializer = TaskSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return JsonResponse(data={}, status=201)


# WE CHANGE THE NAME OF THIS VIEW TO REFLECT THAT IT CAN ALSO CRATE
@csrf_exempt
def get_create_board(request, pk):
    try:
        # We try to retrieve the object with the given pk
        board = TaskBoard.objects.get(id=pk)
    except TaskBoard.DoesNotExist:
        # If we get an exception, namely DoesNotExist, we return a 404
        return JsonResponse({'detail': 'Not found'}, status=404)

    # We return the details of a single item when the HTTP method is GET
    if request.method == 'GET':
        dict_board = TaskBoardSerializer(board).data
        return JsonResponse(dict_board)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        serializer = TaskBoardSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return JsonResponse(data={}, status=200)

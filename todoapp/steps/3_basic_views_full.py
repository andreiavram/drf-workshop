import json
from datetime import date

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from manager.models import Task, TaskBoard


@csrf_exempt
def list_tasks(request):
    """Return a JsonResponse with all Task records in the database"""
    # We list the Tasks only if the HTTP method is GET
    # What do we do when a POST comes in?
    if request.method == 'GET':
        # create a queryset for all the records from the Task model
        tasks = Task.objects.all()

        # transform each task into a dict representation and add it to a list
        dict_tasks = []
        for task in tasks:
            # add the other fields from `task` here
            task_dict = {
                'id': task.id,
                'name': task.name,
                'description': task.description
            }
            dict_tasks.append(task_dict)

        # return a JSON response (sets content type to "application/json")
        return JsonResponse(dict_tasks, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        date_str = data['date']
        if date:
            date_parts = date_str.split('-')
            year = int(date_parts[0])
            month = int(date_parts[1])
            day = int(date_parts[2])

            date_object = date(year, month, day)
        else:
            date_object = None

        task = Task(
            name=data['name'],
            description=data['description'],
            priority=data['priority'],
            board_id=data['board'],
            state=data['state'],
            due_date=date_object
        )

        task.save()

        return JsonResponse(data={}, status=201)


# WE CHANGE THE NAME OF THIS VIEW TO REFLECT THAT IT CAN ALSO CRATE
@csrf_exempt
def get_update_board(request, pk):
    try:
        # We try to retrieve the object with the given pk
        board = TaskBoard.objects.get(id=pk)
    except TaskBoard.DoesNotExist:
        # If we get an exception, namely DoesNotExist, we return a 404
        return JsonResponse({'detail': 'Not found'}, status=404)

    # We return the details of a single item when the HTTP method is GET
    if request.method == 'GET':
        dict_board = {
            'id': board.id,
            'name': board.name
        }

        return JsonResponse(dict_board)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        board.name = data['name']
        board.save()

        return JsonResponse(data={}, status=200)

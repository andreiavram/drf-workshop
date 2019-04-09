from django.http import JsonResponse

from manager.models import Task, TaskBoard


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


def get_board(request, pk):
    # We return the details of a single item when the HTTP method is GET
    if request.method == 'GET':
        try:
            # We try to retrieve the object with the given pk
            board = TaskBoard.objects.get(id=pk)
        except TaskBoard.DoesNotExist:
            # If we get an exception, namely DoesNotExist, we return a 404
            return JsonResponse({'detail': 'Not found'}, status=404)

        dict_board = {
            'id': board.id,
            'name': board.name
        }

        return JsonResponse(dict_board)

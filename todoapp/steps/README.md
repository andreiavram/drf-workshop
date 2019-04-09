1.  Models
    - Hand out the first version of the models
    - Add columns to Task model
    - Create the constants for Priority and TaskState
    - Create model for TaskBoard
    - Create model for Label
2. Admin
    - Hand out the base version of admin.py
    - Register all models in admin
    - Add filters
      ```python
      list_filter = ['column_name']
      ```
    - Add search functionality
    ```python
    search_fields = ['column_name']
    ```
3. Function-based views
    - Hand out base version of views.py
4. URLS
    - Hand out base version of urls.py
3. Function-base views *continued*
    - Explain POST vs GET and request
    - Handle POST in list_task (rename to list_create_task)
    - Handle PUT in get_board
    - Explain the pains of doing this and how Django has a better options, serializers
5. Serializers
    - Hand out base version of serializers.py
    - Create the rest of the serializers for the rest of the models
6. Function-base views with *serializers*
    - Replace the manual serialization with a Serializer
7. Class-based views
    - Hand out base version of the views
    - Create full CRUD for each model, two views per model
    - Create a URL for each path
8. Viewsets
    - Hand out base version for viewsets
9. URLs for viewsets
    - hand out base version of URLs for viewsets
8. Viewsets *continued*
    - Create viewsets for the rest of the models
10. Actions on viewsets
    - Create a done_tasks action that returns only tasks which are in state DONE
      ```python
      @action(detail=False)
      def done_tasks(self, request):
          queryset = Task.objects.filter(state=TaskState.DONE)
          serializer = self.get_serializer(queryset, many=True)

          return Response(serializer.data)
      ```
11. Authentication
    - Add the URL for default DRF auth token view
      Add rest_framework and rest_framework.authtoken to INSTALLED_APPS
      Add REST_FRAMEWORK settings as follows
      ```python
      REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': (
           'rest_framework.permissions.IsAuthenticated',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.TokenAuthentication',
        )
     }
     ```
12. Board default user
    - At Board creation, add the user from request to the board to be created
      Emphasize that DRF lets you intervene in useful point along the default flow
      ```python
      def get_serializer(self, *args, **kwargs):
          data = kwargs.get('data')
          if data is not None:
              data['user'] = self.request.user

          return super().get_serializer(*args, **kwargs)
      ```
13. Permissions
    - Task permission per user on Task detail view (GET with pk in request.kwargs)
14. Query params
    - Add query param filter for board
      ```python
      def filter_queryset(self, queryset):
        board = self.request.GET.get('board')
        if board:
            queryset = queryset.filter(board_id=board)

        return queryset
      ```
15. USE UI
    - Explain CORS
    - Install django-cors-headers
    - Add middleware 'corsheaders.middleware.CorsMiddleware'
    - Add CORS_ORIGIN_ALLOW_ALL=True in settings

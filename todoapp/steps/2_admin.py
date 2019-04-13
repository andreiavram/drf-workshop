# We've said earlier that Django comes with "batteries included". You haven't
# seen anything yet. It also comes with a full-blown UI where you can create,
# update, delete and view the data that your models hold
from django.contrib import admin

from manager.models import Task


# This class is the configuration that dictates how this particular models'
# data will look in the UI and how we can interact with it.
class TaskAdmin(admin.ModelAdmin):

    list_display = ['name']


# This is how we tell Django to use the class TaskAdmin as the UI configuration
# for the UI
admin.site.register(Task, TaskAdmin)

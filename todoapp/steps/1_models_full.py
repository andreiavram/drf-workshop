# Here is where Django defines the base class for all our models
from django.db import models
# Django comes with "batteries included". This means that it provides us
# with lot of code that can help us out-of-the-box, including a User model
# which we are going to use soon enough
from django.contrib.auth.models import User

# requirement: django-colorful==1.2
from colorful.fields import RGBColorField


# Constants, in constants.py
class Priority:

    NONE = 0
    LOWEST = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    MAXIMUM = 5

    CHOICES = [
        (NONE, 'None'),
        (LOWEST, 'Lowest'),
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
        (MAXIMUM, 'Maximum'),
    ]


class TaskState(object):
    ARCHIVED = 0
    ACTIVE = 1
    DONE = 2

    CHOICES = [
        (ARCHIVED, 'Archived'),
        (ACTIVE, 'Active'),
        (DONE, 'Done')
    ]


# Models
class TaskBoard(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=4096, null=True, blank=True)

    def __str__(self):
        return self.name


class Label(models.Model):

    name = models.CharField(max_length=100)
    color = RGBColorField(default='#FFF')

    def __str__(self):
        return self.name


# Defining a model/database table is as simple as creating a new class
# The class attributes are the columns of the table
class Task(models.Model):

    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=5000, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.PositiveSmallIntegerField(choices=Priority.CHOICES, default=Priority.NONE)
    board = models.ForeignKey(TaskBoard, on_delete=models.CASCADE, related_name='items')
    state = models.PositiveSmallIntegerField(choices=TaskState.CHOICES, default=TaskState.ACTIVE)

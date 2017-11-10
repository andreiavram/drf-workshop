from django.db import models

# Create your models here.

class Device(models.Model):
    DEVICE_READ = 1
    DEVICE_WRITE = 0

    DEVICE_DIRECTION = ((DEVICE_READ, "data provider"), (DEVICE_WRITE, "data consumer"))

    name = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    direction = models.IntegerField(choices=DEVICE_DIRECTION)

    def read(self):
        pass

    def write(self, data):
        pass


class MessageHistory(models.Model):
    pass


class RuleSet(models.Model):
    pass


class Rule(models.Model):
    pass
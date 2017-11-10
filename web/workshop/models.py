from django.db import models
import time
import random
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

    def is_alive(self) -> bool:
        #   this simulates an expensive get status operation :)
        time.sleep(1)
        return bool(random.getrandbits(1))


class MessageHistory(models.Model):
    pass


class RuleSet(models.Model):
    pass


class Rule(models.Model):
    pass
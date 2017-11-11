import time
import random

from django.db import models
from django.contrib.auth import get_user_model

from device_client import DeviceController
from workshop.constants import MessageDirection, Operation


class Device(models.Model):

    name = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    direction = models.IntegerField(choices=MessageDirection.DEVICE_DIRECTIONS)
    description = models.TextField(null=True, blank=True)

    def read(self, client=None):
        if self.direction == MessageDirection.DEVICE_WRITE:
            raise ValueError('This device is only for writing')

        if client is not None:
            return client.read(self.topic)

        with DeviceController(self.name) as client:
            return client.read(self.topic)

    def write(self, data, client=None):
        if not all([value.isdigit() for value in data.split(',')]):
            raise ValueError('Data may be only a CSV list of numbers')

        if self.direction == MessageDirection.DEVICE_READ:
            raise ValueError('This device is only for reading')

        if client is not None:
            client.send(self.topic, data)
        else:
            with DeviceController(self.name) as client:
                client.send(self.topic, data)

    def is_alive(self) -> bool:
        #   this simulates an expensive get status operation :)
        time.sleep(1)
        return bool(random.getrandbits(1))

    def __str__(self):
        return self.name


class MessageHistory(models.Model):

    device = models.ForeignKey(Device)
    value = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model())


class RuleSet(models.Model):

    target_device = models.ForeignKey(Device)
    payload = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return 'Device: {}. Payload: {}'.format(
            self.target_device, self.payload)


class Rule(models.Model):

    ruleset = models.ForeignKey(RuleSet, related_name='rules')
    source_device = models.ForeignKey(Device)
    ref_value = models.FloatField()
    operator = models.CharField(max_length=10, choices=Operation.OPERATIONS)

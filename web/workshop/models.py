import time
import random

from django.db import models
from device_client import DeviceController

from workshop.constants import MessageDirection, Operation


class Device(models.Model):

    name = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    direction = models.IntegerField(choices=MessageDirection.DEVICE_DIRECTIONS)
    description = models.TextField(null=True, blank=True)

    def read(self):
        if self.direction == self.DEVICE_WRITE:
            raise ValueError('This device is only for writing')

        with DeviceController(self.name) as device:
            return device.read(self.topic)

    def write(self, data):
        if not all([value.isdigit() for value in data.split(',')]):
            raise ValueError('Data may be only a CSV list of numbers')

        if self.direction == self.DEVICE_READ:
            raise ValueError('This device is only for reading')

        with DeviceController(self.name) as device:
            device.write(self.topic, data)

    def is_alive(self) -> bool:
        #   this simulates an expensive get status operation :)
        time.sleep(1)
        return bool(random.getrandbits(1))

    def __str__(self):
        return self.name


class MessageHistory(models.Model):

    device = models.ForeignKey(Device)
    value = models.CharField(max_length=100)


class RuleSet(models.Model):

    target_device = models.ForeignKey(Device)
    payload = models.CharField(max_length=100)

    def __str__(self):
        return 'Device: {}. Payload: {}'.format(
            self.target_device, self.payload)


class Rule(models.Model):

    ruleset = models.ForeignKey(RuleSet, related_name='rules')
    source_device = models.ForeignKey(Device)
    ref_value = models.FloatField()
    operator = models.SmallIntegerField(choices=Operation.OPERATIONS)

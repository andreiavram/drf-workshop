import random
import time

from django.core.management import BaseCommand
from device_client import DeviceController

from workshop.models import MessageHistory, Device
from workshop.constants import MessageDirection, Operation


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval', dest='interval', action='store', default=1)

    def run(self, interval=1):
        past_time = 0
        read_devices = Device.objects.filter(
            direction=MessageDirection.DEVICE_READ)
        while True:
            if past_time >= 5:
                self.stdout.write('Loading devices again ...')
                read_devices = Device.objects.filter(
                    direction=MessageDirection.DEVICE_READ)
                past_time = 0

            for device in read_devices:
                value = device.read(client=self.device_ctrl)
                self.stdout.write(
                    'Read [{}] from [{}].'.format(value, device.name))
                MessageHistory.objects.create(device=device, value=value)

            time.sleep(interval)
            past_time += interval

    def handle(self, *args, **options):
        options['interval'] = float(options['interval'])
        self.device_ctrl = DeviceController(
            'rules_runner_{}'.format(random.randint(0, 1000)))
        self.device_ctrl.start()

        try:
            self.run(interval=options['interval'])
        except KeyboardInterrupt:
            self.stdout.write('Exit by used. B-Bye.')
        finally:
            self.device_ctrl.stop()

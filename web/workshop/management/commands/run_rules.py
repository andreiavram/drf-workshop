import random
import time

from django.core.management import BaseCommand
from device_client import DeviceController

from workshop.models import RuleSet
from workshop.constants import MessageDirection, Operation


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval', dest='interval', action='store', default=1)

    def evaluate_rule(self, rule):
        if rule.source_device.direction == MessageDirection.DEVICE_WRITE:
            raise ValueError('A rule may only be for a DEVICE_READ')

        value = rule.source_device.read(client=self.device_ctrl)

        return Operation.eval_for_op(rule.operator, value, rule.ref_value)

    def run(self, interval=1):
        past_time = 0
        rule_sets = RuleSet.objects.all()
        while True:
            if past_time >= 5:
                self.stdout.write('Loading rule sets again ...')
                rule_sets = RuleSet.objects.all()
                past_time = 0

            for rule_set in rule_sets:
                is_met = all([
                    self.evaluate_rule(rule) for rule in rule_set.rules.all()
                ])
                if is_met:
                    rule_set.target_device.write(
                        rule_set.payload, client=self.device_ctrl)
                    self.stdout.write(
                        'RuleSet [[{}]] has been triggered.'.format(rule_set)
                    )

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

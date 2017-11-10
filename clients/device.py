import random
import time

import paho.mqtt.client as mqtt


class DeviceController(object):

    def __init__(self, uid, host='mqtt.acandale.com', port=1884):
        self.uid = '{}_{}'.format(uid, random.randint(0, 500))
        self.client = mqtt.Client(self.uid)
        self.host = host
        self.port = port
        self.messages = {}

    def start(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.host, self.port, 60)
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()

    def on_message(self, client, userdata, msg):
        self.messages[msg.topic] = msg.payload

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe('device/#')

    def send(self, device, payload):
        self.client.publish(device, payload)

    def get_message(self, device, retries=3, delay=0.5):
        counter = 0
        while True:
            if device in self.messages:
                return self.messages[device]
            counter += 1
            if counter >= retries:
                raise ValueError('No message from device: {}'.format(device))
            time.sleep(delay)

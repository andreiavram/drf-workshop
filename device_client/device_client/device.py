import ssl
import time
import random

import paho.mqtt.client as mqtt


class DeviceController(object):
    """
    Exposes two operations: read an write. The read operations get data
    from topic device/<device_name> while the write operations are performed
    on topic device/c/<device_name>
    """

    def __init__(
            self, uid, host='mqtt.acandale.com', port=1884,
            mqtt_user=None, mqtt_pass=None, tls=False):
        self.uid = '{}_{}'.format(uid, random.randint(0, 500))
        self.client = mqtt.Client(self.uid)
        if mqtt_user and mqtt_pass:
            self.client.username_pw_set(mqtt_user, mqtt_pass)

        if tls:
            self.client.tls_set_context(ssl.create_default_context())

        self.host = host
        self.port = port
        self.messages = {}

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def start(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        print(self.client.connect(self.host, self.port, 60))
        print(self.client.loop_start())

    def stop(self):
        self.client.loop_stop()

    def on_message(self, client, userdata, msg):
        # if 'device/c/' in msg.topic:
        #     return

        self.messages[msg.topic] = msg.payload.decode('ascii')

    def on_connect(self, client, userdata, flags, rc):
        print('connected')
        print(self.client.subscribe('device/#'))

    def send(self, device, payload):
        self.client.publish('device/c/{}'.format(device), payload, qos=1)

    def read(self, device, retries=3, delay=0.5):
        counter = 0
        topic = 'device/{}'.format(device)
        while True:
            if topic in self.messages:
                try:
                    return float(self.messages[topic])
                except ValueError:
                    return self.messages[topic]
            counter += 1
            if counter >= retries:
                raise ValueError('No message from device: {}'.format(device))
            time.sleep(delay)

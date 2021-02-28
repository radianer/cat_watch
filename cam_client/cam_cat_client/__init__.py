import cv2 as cv
import base64
import paho.mqtt.client as mqtt
import numpy as np

class CamCatClient:

    def __init__(self, mqtt_broker, mqtt_topic):
        self.mqtt_broker = mqtt_broker
        self.mqtt_topic = mqtt_topic
        self.output_frame = None
        self.client = None

    def start(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.mqtt_broker)
        client.loop_start()
        self.client = client
    
    def stop(self):
        self.client.loop_stop()

    def on_message(self, client, userdata, msg):
        if msg.topic == self.mqtt_topic:
            img = base64.b64decode(msg.payload)
            npimg = np.frombuffer(img, dtype=np.uint8)
            frame = cv.imdecode(npimg, 1)
            self.output_frame = frame.copy()

    def on_connect(self, client, userdata, flags, rc):
        print("Connect")
        client.subscribe(self.mqtt_topic)
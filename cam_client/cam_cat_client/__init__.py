import cv2 as cv
import base64
import paho.mqtt.client as mqtt
import numpy as np

MQTT_TOPIC_ORG = "front/door/org"
MQTT_TOPIC_DETECT = "front/door/detect"
MQTT_TOPIC_DELTA = "front/door/delta"
MQTT_TOPIC_THRESH = "front/door/thresh"

class CamCatClient:

    def __init__(self, mqtt_broker):
        self.mqtt_broker = mqtt_broker
        self.output_org = None
        self.output_delta = None
        self.output_detect = None
        self.output_thresh = None
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
        global MQTT_TOPIC_ORG, MQTT_TOPIC_DELTA, MQTT_TOPIC_DETECT

        img = base64.b64decode(msg.payload)
        npimg = np.frombuffer(img, dtype=np.uint8)
        frame = cv.imdecode(npimg, 1)

        if msg.topic == MQTT_TOPIC_ORG:
            self.output_org = frame.copy()
        elif msg.topic == MQTT_TOPIC_DELTA:
            self.output_delta = frame.copy()
        elif msg.topic == MQTT_TOPIC_DETECT:
            self.output_detect = frame.copy()
        elif msg.topic == MQTT_TOPIC_THRESH:
            self.output_thresh = frame.copy()

    def on_connect(self, client, userdata, flags, rc):
        global MQTT_TOPIC_ORG, MQTT_TOPIC_DELTA, MQTT_TOPIC_DETECT
        print("Connect")
        client.subscribe(MQTT_TOPIC_ORG)
        client.subscribe(MQTT_TOPIC_DELTA)
        client.subscribe(MQTT_TOPIC_DETECT)
import cv2 as cv
import base64
import paho.mqtt.client as mqtt
import numpy as np
import json
import time

MQTT_DOOR_PREFIX = "back"

MQTT_TOPIC_ORG = MQTT_DOOR_PREFIX + "/door/org"
MQTT_TOPIC_DELTA = MQTT_DOOR_PREFIX + "/door/delta"
MQTT_TOPIC_DETECT = MQTT_DOOR_PREFIX + "/door/detect"
MQTT_TOPIC_THRESH = MQTT_DOOR_PREFIX + "/door/thresh"
MQTT_TOPIC_BOXES = MQTT_DOOR_PREFIX + "/door/boxes"
MQTT_TOPIC_CALIBRATE = MQTT_DOOR_PREFIX + "/door/calibrate"

class CamCatClient:

    def __init__(self, mqtt_broker, detection_processor):
        self.mqtt_broker = mqtt_broker
        self.output_org = None
        self.output_delta = None
        self.output_detect = None
        self.output_thresh = None
        self.client = None
        self.detect_processor = detection_processor

    def start(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.mqtt_broker)
        client.loop_start()
        self.client = client
    
    def stop(self):
        self.client.loop_stop()

    def send_calibrate(self):
        self.detect_processor.calibrate(self.output_org)

    def on_message(self, client, userdata, msg):
        global MQTT_TOPIC_ORG, MQTT_TOPIC_DELTA, MQTT_TOPIC_DETECT, MQTT_TOPIC_THRESH, MQTT_TOPIC_BOXES

        start = time.time()
        img = base64.b64decode(msg.payload)
        npimg = np.frombuffer(img, dtype=np.uint8)
        frame = cv.imdecode(npimg, 1)


        if msg.topic == MQTT_TOPIC_ORG:
            self.output_org = frame.copy()
            self.process_img(frame)

        end = time.time()
        print("Dauer:", end - start)

    def process_img(self, img):
        rects, self.output_detect, self.output_delta, self.output_thresh = self.detect_processor.detect(img)
        pass
    
    def on_boxes(self, payload):
        start = time.time()
        print("Decode")
        utf = payload.decode("utf-8","ignore")
        # print(payload)
        obj = json.loads(utf)
        print(obj["boxes"])
        end = time.time()
        print("decode end:", end - start)

    def on_connect(self, client, userdata, flags, rc):
        global MQTT_TOPIC_ORG, MQTT_TOPIC_DELTA, MQTT_TOPIC_DETECT, MQTT_TOPIC_THRESH, MQTT_TOPIC_BOXES
        print("Connect")
        client.subscribe(MQTT_TOPIC_ORG)
    
    def get_org(self):
        return self.output_org
    
    def get_delta(self):
        return self.output_delta
    
    def get_detect(self):
        return self.output_detect
    
    def get_thresh(self):
        return self.output_thresh
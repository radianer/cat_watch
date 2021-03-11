"""
@author Radianer
"""
import cv2 as cv
import paho.mqtt.client as mqtt
import base64
import time

MQTT_DOOR_PREFIX = "back"

MQTT_TOPIC_ORG = MQTT_DOOR_PREFIX + "/door/org"
MQTT_TOPIC_DELTA = MQTT_DOOR_PREFIX + "/door/delta"
MQTT_TOPIC_DETECT = MQTT_DOOR_PREFIX + "/door/detect"
MQTT_TOPIC_THRESH = MQTT_DOOR_PREFIX + "/door/thresh"
MQTT_TOPIC_BOXES = MQTT_DOOR_PREFIX + "/door/boxes"
MQTT_TOPIC_CALIBRATE = MQTT_DOOR_PREFIX + "/door/calibrate"

class CamCatWatch:
    
    def __init__(self, cam_id, resolution, mqtt_broker, min_area):
        self.cam_id = cam_id
        self.resolution = resolution
        self.mqtt_broker = mqtt_broker
        self.running = True
        self.client = None
        self.last_frame = None
        self.min_area = min_area
        self.calibrate = True

    def on_message(self, client, userdata, msg):
        global MQTT_TOPIC_CALIBRATE

        if msg.topic == MQTT_TOPIC_CALIBRATE:
            self.calibrate = True
            print("Message")
            print(msg.payload)
    
    def on_connect(self, client, userdata, flags, rc):
        global MQTT_TOPIC_CALIBRATE
        print("Connect")
        client.subscribe(MQTT_TOPIC_CALIBRATE)

    def start(self):
        global MQTT_TOPIC_ORG
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.mqtt_broker)
        client.loop_start()
        self.client = client

        cap = cv.VideoCapture(self.cam_id)
        cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        cap.set(cv.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        
        print("Init")
        for i in range(10):
            print(str(i) + " init frame")
            ret, frame = cap.read()
            time.sleep(1)

        ret, frame = cap.read()
        gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        self.last_frame = gray_img

        while self.running:
            start = time.time()
            ret, frame = cap.read()
            if not ret:
                print("Fail to read")
                continue
            self.send_img(MQTT_TOPIC_ORG, frame.copy())
            end = time.time()
            print("Dauer:", end - start)
            time.sleep(1)
    
    def stop(self):
        self.running = False
        self.client.loop_stop()

    def send_img(self, topic, frame):
        ret, buffer = cv.imencode(".jpg", frame)
        if not ret:
            print("Fail to encode")
        jpg_base = base64.b64encode(buffer)
        self.client.publish(topic, jpg_base)
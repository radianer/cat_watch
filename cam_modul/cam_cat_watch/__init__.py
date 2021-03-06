"""
@author Radianer
"""
import numpy as np
import cv2 as cv
import paho.mqtt.client as mqtt
import base64
import imutils
import json
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
            ret, frame = cap.read()
            if not ret:
                print("Fail to read")
                continue
            self.send_img(MQTT_TOPIC_ORG, frame.copy())
            self.motion_detection(frame)
            time.sleep(1)
    
    def stop(self):
        self.running = False
        self.client.loop_stop()

    def motion_detection(self, frame):
        global MQTT_TOPIC_DELTA, MQTT_TOPIC_DETECT, MQTT_TOPIC_THRESH
        frame = frame.copy()
        gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray_img = cv.GaussianBlur(gray_img, (21,21), 0)
        if self.last_frame is None:
            self.last_frame = gray_img
            return
        
        frame_delta = cv.absdiff(self.last_frame, gray_img)
        # self.send_img(MQTT_TOPIC_DELTA, frame_delta)
        _, thresh = cv.threshold(frame_delta, 25, 255, cv.THRESH_BINARY)

        thresh = cv.dilate(thresh, None, iterations=2)
        # self.send_img(MQTT_TOPIC_THRESH, thresh)

        cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        
        rects = []
        for c in cnts:
            if cv.contourArea(c) < self.min_area:
                continue
            
            (x, y, w, h) = cv.boundingRect(c)
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            rects.append([x, y, x+w, y+h])
        
        # rects = tuple(rects)

        # obj_rects = {rects: tuple(rects)}

        # self.send_img(MQTT_TOPIC_DETECT, frame)
        if len(rects) == 0 or self.calibrate:
            self.last_frame = gray_img
            self.calibrate = False
        else:
            self.send_obj(MQTT_TOPIC_BOXES, rects)

    def send_obj(self, topic, obj):
        json_dump = json.dumps(obj)
        self.client.publish(topic, json_dump)

    def send_img(self, topic, frame):
        ret, buffer = cv.imencode(".jpg", frame)
        if not ret:
            print("Fail to encode")
        jpg_base = base64.b64encode(buffer)
        self.client.publish(topic, jpg_base)
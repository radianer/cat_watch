"""
@author Radianer
"""
import numpy as np
import cv2 as cv
import threading
import paho.mqtt.client as mqtt
import base64
import imutils
import json

MQTT_DOOR_PREFIX = "back"

MQTT_TOPIC_ORG = MQTT_DOOR_PREFIX + "/door/org"
MQTT_TOPIC_DELTA = MQTT_DOOR_PREFIX + "/door/delta"
MQTT_TOPIC_DETECT = MQTT_DOOR_PREFIX + "/door/detect"
MQTT_TOPIC_THRESH = MQTT_DOOR_PREFIX + "/door/thresh"
MQTT_TOPIC_BOXES = MQTT_DOOR_PREFIX + "/door/boxes"

class CamCatWatch:
    
    def __init__(self, cam_id, resolution, mqtt_broker, min_area):
        self.cam_id = cam_id
        self.resolution = resolution
        self.mqtt_broker = mqtt_broker
        self.running = True
        self.client = None
        self.lastFrame = None
        self.min_area = min_area

    def start(self):
        global MQTT_TOPIC_ORG
        client = mqtt.Client()
        client.connect(self.mqtt_broker)
        self.client = client

        cap = cv.VideoCapture(self.cam_id)
        cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        cap.set(cv.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        
        while self.running:
            ret, frame = cap.read()
            if not ret:
                print("Fail to read")
                continue
            self.send_img(MQTT_TOPIC_ORG, frame.copy())
            self.motion_detection(frame)

    def motion_detection(self, frame):
        global MQTT_TOPIC_DELTA, MQTT_TOPIC_DETECT, MQTT_TOPIC_THRESH
        frame = frame.copy()
        gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray_img = cv.GaussianBlur(gray_img, (21,21), 0)
        if self.lastFrame is None:
            self.lastFrame = gray_img
            return
        
        frame_delta = cv.absdiff(self.lastFrame, gray_img)
        self.send_img(MQTT_TOPIC_DELTA, frame_delta)
        _, thresh = cv.threshold(frame_delta, 25, 255, cv.THRESH_BINARY)

        thresh = cv.dilate(thresh, None, iterations=2)
        self.send_img(MQTT_TOPIC_THRESH, thresh)

        cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        
        rects = []
        for c in cnts:
            if cv.contourArea(c) < self.min_area:
                continue
            
            (x, y, w, h) = cv.boundingRect(c)
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            rects.append([x, y, x+w, y+h])

        self.send_array(MQTT_TOPIC_BOXES, rects)
        self.send_img(MQTT_TOPIC_DETECT, frame)
        self.lastFrame = gray_img

    def send_array(self, topic, array):
        if len(array) > 0:
            a = np.array(array)
            l = a.tolist()
            dump = json.dumps(array)
            self.client.publish(topic, array)

    def send_img(self, topic, frame):
        ret, buffer = cv.imencode(".jpg", frame)
        if not ret:
            print("Fail to encode")
        jpg_base = base64.b64encode(buffer)
        self.client.publish(topic, jpg_base)
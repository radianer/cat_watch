"""
@author Radianer
"""
import cv2 as cv
import threading
import paho.mqtt.client as mqtt
import base64

class CamCatWatch:
    
    def __init__(self, cam_id, resolution, mqtt_broker, mqtt_topic):
        self.cam_id = cam_id
        self.resolution = resolution
        self.mqtt_broker = mqtt_broker
        self.mqtt_topic = mqtt_topic
        self.running = True

    def start(self):
        client = mqtt.Client()
        client.connect(self.mqtt_broker)

        cap = cv.VideoCapture(self.cam_id)
        cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        cap.set(cv.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        
        while self.running:
            ret, frame = cap.read()
            if not ret:
                print("Fail to read")
                continue
            ret, buffer = cv.imencode(".jpg", frame)
            if not ret:
                print("Fail to encode")
            
            jpg_base = base64.b64encode(buffer)
            client.publish(self.mqtt_topic, jpg_base)

"""
@author Radianer
"""
import cv2 as cv
import base64
import time
import numpy as np
import socket
import pickle
import struct

class CamCatWatchTCP:
    
    def __init__(self, cam_id, resolution, min_area, server_ip, server_port):
        self.cam_id = cam_id
        self.resolution = resolution
        self.min_area = min_area
        self.server_ip = server_ip
        self.server_port = server_port

        self.running = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.last_frame = None
        self.calibrate = True

    def start(self):
        
        self.socket.connect((self.server_ip, self.server_port))
        print("Connected")

        cap = cv.VideoCapture(self.cam_id)
        cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        cap.set(cv.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        
        print("Init")
        for i in range(5):
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
            self.send_img(frame.copy())
            end = time.time()
            print("Dauer:", end - start)
            time.sleep(10)
    
    def stop(self):
        self.running = False

    def send_img(self, frame):
        ret, buffer = cv.imencode(".jpg", frame)
        if not ret:
            print("Fail to encode")
        data = pickle.dumps(buffer, 0)
        size = len(data)
        self.socket.sendall(struct.pack(">L", size) + data)
        # jpg_base = base64.b64encode(buffer)
        # self.socket.send(jpg_base)

        
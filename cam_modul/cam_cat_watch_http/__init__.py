"""
@author Radianer
"""
import cv2 as cv
import time
import requests
import pickle

class CamCatWatchHTTP:
    
    def __init__(self, cam_id, resolution, interval, min_area, server_ip, server_port):
        self.cam_id = cam_id
        self.resolution = resolution
        self.interval = interval
        self.min_area = min_area
        self.server_ip = server_ip
        self.server_port = server_port
        self.url = "http://{}:{}/image".format(server_ip, server_port)

        self.running = True
        self.last_frame = None
        self.calibrate = True

    def start(self):
        
        print("Start take images")

        cap = cv.VideoCapture(self.cam_id)
        cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        cap.set(cv.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.resolution[1])

        start_time = time.time()
        while self.running:
            ret, frame = cap.read()
            if not ret:
                print("Fail to read")
                continue
            if time.time() - start_time >= 5:
                start_time = time.time()
                start = time.time()
                self.send_img(frame.copy())
                end = time.time()
                print("Dauer:", end - start)
    
    def stop(self):
        self.running = False

    def send_img(self, frame):
        ret, buffer = cv.imencode(".jpg", frame)
        if not ret:
            print("Fail to encode")
        data = pickle.dumps(buffer, 0)
        size = len(data)
        try:
            requests.post(self.url, data)
        except:
            print("No Connection!!!")

        
from flask import Flask, request
import cv2 as cv
import pickle
import threading

class Server:

    def __init__(self, port):
        self.port = port
        self.app = Flask(__name__)
        self.app.add_url_rule("/image", "post_image", self.post_image, methods=["POST"])
        self.app.add_url_rule("/image", "get_image", self.get_image, methods=["GET"])
        self.running = False
        self.running_t = None
        self.image = None
        self.frame_data = None
        self.is_new_image = False

    
    def post_image(self):
        print("POST")
        self.frame_data = request.data
        frame = pickle.loads(self.frame_data, fix_imports=True, encoding="bytes")
        self.image = cv.imdecode(frame, cv.IMREAD_COLOR)
        self.is_new_image = True
        # cv.imshow("Frame", self.image)
        # cv.waitKey(1)
        return "OK", 200
    
    def get_image(self):
        print("GET")
        if(self.frame_data is None) :
            return "No Image", 204
        
        return self.frame_data, 200
    
    def get_images(self):
        while self.running:
            if self.is_new_image:
                self.is_new_image = False
                yield self.image



    def start(self):
        self.running = True
        self.running_t = threading.Thread(target=self.__start)
        self.running_t.start()
    
    def __start(self):
        self.app.run(port=self.port, host="0.0.0.0")

"""
@author Radianer
"""
import cv2 as cv
import threading


LOCK = threading.Lock()

class CamCatWatch:
    
    def __init__(self, cam_id):
        self.cam_id = cam_id
        self.running = True
        self.output_frame = None
        self.t = threading.Thread(target=self.loop, args=())
        self.t.daemon = True
        self.t.start()
        pass

    def loop(self):
        global LOCK
        cap = cv.VideoCapture(self.cam_id)
        cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
        
        while self.running:
            ret, frame = cap.read()
            if not ret:
                print("Fail to read frame")
                continue

            with LOCK:
                self.output_frame = frame.copy()

    def gen_frames(self):
        global LOCK

        while self.running:
            with LOCK:
                if self.output_frame is None:
                    continue

                ret, buffer = cv.imencode(".jpg", self.output_frame)
                if not ret:
                    print("Failt to encode")
                    continue
                frame = buffer.tobytes()
                yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        pass

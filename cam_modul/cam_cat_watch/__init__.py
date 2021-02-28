"""
@author Radianer
"""
import cv2 as cv


class CamCatWatch:
    
    def __init__(self, cap):
        self.cap = cap
        pass

    def gen_frames(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Fail to read frame")
                break
            ret, buffer = cv.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        pass

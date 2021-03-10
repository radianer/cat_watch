import cv2 as cv
import imutils

class CatDetect:

    def __init__(self, min_area):
        self.last_img_gray = None
        self.min_area = min_area

    def calibrate(self, img):
        img = img.copy()
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        gray_img = cv.GaussianBlur(gray_img, (21,21), 0)
        self.last_img_gray = gray_img

    def detect(self, img):
        return self.motio_detection(img)

    def motio_detection(self, img):
        org_img = img.copy()
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        gray_img = cv.GaussianBlur(gray_img, (21,21), 0)
        if self.last_img_gray is None:
            self.last_img_gray = gray_img
            return None, None, None, None
        
        frame_delta = cv.absdiff(self.last_img_gray, gray_img)

        _, thresh = cv.threshold(frame_delta, 25, 255, cv.THRESH_BINARY)

        thresh= cv.dilate(thresh, None, iterations=2)

        cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        frame_rect = img.copy()
        rects = []
        for c in cnts:
            if cv.contourArea(c) < self.min_area:
                continue
            
            (x, y, w, h) = cv.boundingRect(c)
            cv.rectangle(frame_rect, (x, y), (x + w, y + h), (0, 255, 0), 2)
            rects.append([x, y, x+w, y+h])
        
        if len(rects) == 0:
            self.last_img_gray = gray_img
        
        return rects, frame_rect, cv.cvtColor(frame_delta, cv.COLOR_GRAY2BGR), cv.cvtColor(thresh, cv.COLOR_GRAY2BGR)
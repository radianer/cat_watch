"""
@author Radianer
"""
from cam_cat_watch import CamCatWatch
from cam_cat_server import CamCatServer
import cv2 as cv

CAM_ID = 0

if __name__ == "__main__":
    print("start")
    cap = cv.VideoCapture(CAM_ID)
    cat_watcher = CamCatWatch(cap)
    server = CamCatServer(cat_watcher)
    server.run()
"""
@author Radianer
"""
from cam_cat_watch import CamCatWatch
from cam_cat_server import CamCatServer
import cv2 as cv

CAM_ID = 0
FRAME_RESOLUTION = [1920, 1080]

if __name__ == "__main__":
    print("start")
    cap = cv.VideoCapture(CAM_ID)
    cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    cap.set(cv.CAP_PROP_FRAME_WIDTH, FRAME_RESOLUTION[0])
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, FRAME_RESOLUTION[1])
    cat_watcher = CamCatWatch(cap)
    server = CamCatServer(cat_watcher)
    server.run()
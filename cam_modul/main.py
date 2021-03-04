"""
@author Radianer
"""
from cam_cat_watch import CamCatWatch
import cv2 as cv
import sys

CAM_ID = 0
FRAME_RESOLUTION = [1920, 1080]
MQTT_BROKER = "192.168.178.27"
MIN_AREA = 200

if __name__ == "__main__":
    while True:
        print("start")
        cat_watcher = CamCatWatch(CAM_ID, FRAME_RESOLUTION, MQTT_BROKER, MIN_AREA)
        cat_watcher.start()
        # try:
        #     print("start")
        #     cat_watcher = CamCatWatch(CAM_ID, FRAME_RESOLUTION, MQTT_BROKER, MIN_AREA)
        #     cat_watcher.start()
        # except:
        #     print("Exception")
        #     print(sys.exc_info()[0])
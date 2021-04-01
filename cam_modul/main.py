"""
@author Radianer
"""
from cam_cat_watch_mqtt import CamCatWatchMQTT
from cam_cat_watch_tcp import CamCatWatchTCP
from cam_cat_watch_http import CamCatWatchHTTP
import cv2 as cv
import sys

CAM_ID = 0
FRAME_RESOLUTION = [1920, 1080]
# FRAME_RESOLUTION = [960, 540]
# MQTT_BROKER = "192.168.178.27"
# SERVER_IP = "localhost"
SERVER_IP = "192.168.178.40"
SERVER_PORT = 5000
MIN_AREA = 200
INTERVAL = 5

if __name__ == "__main__":
    while True:
        print("start")
        # cat_watcher = CamCatWatchMQTT(CAM_ID, FRAME_RESOLUTION, MQTT_BROKER, MIN_AREA)
        # cat_watcher.start()
        # cat_watcher = CamCatWatchTCP(CAM_ID, FRAME_RESOLUTION, INTERVAL, MIN_AREA, SERVER_IP, SERVER_PORT)
        cat_watcher = CamCatWatchHTTP(CAM_ID, FRAME_RESOLUTION, INTERVAL, MIN_AREA, SERVER_IP, SERVER_PORT)
        cat_watcher.start()
        # try:
        #     print("start")
        #     cat_watcher = CamCatWatch(CAM_ID, FRAME_RESOLUTION, MQTT_BROKER, MIN_AREA)
        #     cat_watcher.start()
        # except:
        #     print("Exception")
        #     print(sys.exc_info()[0])
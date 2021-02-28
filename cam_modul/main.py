"""
@author Radianer
"""
from cam_cat_watch import CamCatWatch
from cam_cat_server import CamCatServer
import cv2 as cv

CAM_ID = 0
FRAME_RESOLUTION = [1920, 1080]
MQTT_BROKER = "192.168.178.27"
MQTT_TOPIC = "front/door/cam"

if __name__ == "__main__":
    print("start")
    cat_watcher = CamCatWatch(CAM_ID, FRAME_RESOLUTION, MQTT_BROKER, MQTT_TOPIC)
    cat_watcher.start()
import cv2 as cv
from cam_cat_client import CamCatClient
from cam_cat_window_kivy import CamCatWindowKivy
from cat_detect_processor import CatDetect

MQTT_BROKER = "192.168.178.27"

if __name__ == "__main__":
    print("Start Client")
    detection_processor = CatDetect(200)
    client = CamCatClient(MQTT_BROKER, detection_processor)
    client.start()

    # window = CamCatWindowTk(client)
    # window = CamCatWindowKivy(client)
    # window.start()
    CamCatWindowKivy(client).run()

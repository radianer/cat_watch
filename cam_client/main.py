import cv2 as cv
from cam_cat_client import CamCatClient
from cam_cat_window_Tk import CamCatWindowTk
from cam_cat_window_kivy import CamCatWindowKivy

MQTT_BROKER = "192.168.178.27"

if __name__ == "__main__":
    print("Start Client")
    client = CamCatClient(MQTT_BROKER)
    client.start()

    # window = CamCatWindowTk(client)
    # window = CamCatWindowKivy(client)
    # window.start()
    CamCatWindowKivy(client).run()

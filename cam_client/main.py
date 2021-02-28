import cv2 as cv
from cam_cat_client import CamCatClient

MQTT_BROKER = "192.168.178.27"
MQTT_TOPIC = "front/door/cam"

if __name__ == "__main__":
    print("Start Client")
    client = CamCatClient(MQTT_BROKER, MQTT_TOPIC)
    client.start()

    while True:
        if client.output_frame is not None:
            cv.imshow("Live", client.output_frame)
            
        if cv.waitKey(1) == ord('x'):
            break
    
    client.stop()

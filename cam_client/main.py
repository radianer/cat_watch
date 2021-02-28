import cv2 as cv
from cam_cat_client import CamCatClient

MQTT_BROKER = "192.168.178.27"

if __name__ == "__main__":
    print("Start Client")
    client = CamCatClient(MQTT_BROKER)
    client.start()

    while True:
        if client.output_org is not None:
            cv.imshow("ORG", client.output_org)
        
        if client.output_delta is not None:
            cv.imshow("delta", client.output_delta)
        
        if client.output_detect is not None:
            cv.imshow("detect", client.output_detect)

        if cv.waitKey(1) == ord('x'):
            break
    
    client.stop()

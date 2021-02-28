import cv2 as cv

cap = cv.VideoCapture(0)

cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)

while True:
    ret, frame = cap.read()

    cv.imshow("vid", frame)

    if cv.waitKey(1) == ord("x"):
        break
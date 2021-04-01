import cv2 as cv

class ImageProcessor():

    def __init__(self, server):
        self.server = server
        pass

    def display_images(self):
        images = self.server.get_images()
        for image in images:
            cv.imshow("Frame", image)
            cv.waitKey(1)

    
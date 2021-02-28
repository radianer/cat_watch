from threading import Thread
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import imutils

class CamCatWindow:

    def __init__(self, cam_cat_client):
        self.cam_cat_client = cam_cat_client
        self.root = tki.Tk()
        self.root.wm_title("Cat Watch")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.on_close)
        self.is_run = True
        self.loop_thread = threading.Thread(target=self.loop, args=())

        self.label_org = None
        self.label_detect = None
        self.label_delta = None
        self.label_thresh = None


    def loop(self):
        while self.is_run:
            if self.cam_cat_client.output_org is not None:
                self.set_org_image(self.cam_cat_client.output_org)
        
            if self.cam_cat_client.output_delta is not None:
                self.set_delta_image(self.cam_cat_client.output_delta)
            
            if self.cam_cat_client.output_detect is not None:
                self.set_detect_image(self.cam_cat_client.output_detect)
                pass
            if self.cam_cat_client.output_thresh is not None:
                self.set_thresh_image(self.cam_cat_client.output_thresh)
            pass

    def set_org_image(self, img):
        img = self.convert_image(img)

        if self.label_org is None:
            self.label_org = tki.Label(image=img)
            self.label_org.image = img
            self.label_org.grid(row=0, column=0, padx='5', pady='5', sticky='ew')
        else:
            self.label_org.configure(image=img)
            self.label_org.image = img
        pass

    def set_detect_image(self, img):
        img = self.convert_image(img)

        if self.label_detect is None:
            self.label_detect = tki.Label(image=img)
            self.label_detect.image = img
            self.label_detect.grid(row=0, column=1, padx='5', pady='5', sticky='ew')
        else:
            self.label_detect.configure(image=img)
            self.label_detect.image = img
        pass

    def set_delta_image(self, img):
        img = self.convert_image(img)

        if self.label_delta is None:
            self.label_delta = tki.Label(image=img)
            self.label_delta.image = img
            self.label_delta.grid(row=1, column=0, padx='5', pady='5', sticky='ew')
        else:
            self.label_delta.configure(image=img)
            self.label_delta.image = img
        pass

    def set_thresh_image(self, img):
        img = self.convert_image(img)

        if self.label_thresh is None:
            self.label_thresh = tki.Label(image=img)
            self.label_thresh.image = img
            self.label_thresh.grid(row=1, column=1, padx='5', pady='5', sticky='ew')
        else:
            self.label_thresh.configure(image=img)
            self.label_thresh.image = img
        pass

    def convert_image(self, img):
        img = imutils.resize(img, width=800)
        img = imutils.opencv2matplotlib(img)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        return img


    def on_close(self):
        self.is_run = False
        self.cam_cat_client.stop()
        self.root.quit()

    def start(self):
        self.loop_thread.start()
        self.root.mainloop()

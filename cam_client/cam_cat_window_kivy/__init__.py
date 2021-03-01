from threading import Thread
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.gridlayout import GridLayout
import cv2 as cv

class KivyLiveImage(Image):

    def __init__(self, get_image_function, **kwargs):
        super().__init__(**kwargs)
        self.get_image_function = get_image_function
        Clock.schedule_interval(self.update, 1.0 / 30)
    
    def update(self, dt):
        img = self.get_image_function()
        if img is not None:
            buf = cv.flip(img, 0)
            buf = buf.tostring()
            img_texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
            img_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = img_texture

class CamCatWindowKivy(App):

    def __init__(self, cam_cat_client):
        super(CamCatWindowKivy, self).__init__()
        self.cam_client = cam_cat_client
        self.label_org = None
        self.label_detect = None
        self.label_delta = None
        self.label_thresh = None

    def build(self):
        layout = GridLayout(cols = 2)
        layout.add_widget(KivyLiveImage(get_image_function=self.cam_client.get_org))
        layout.add_widget(KivyLiveImage(get_image_function=self.cam_client.get_detect))
        layout.add_widget(KivyLiveImage(get_image_function=self.cam_client.get_delta))
        layout.add_widget(KivyLiveImage(get_image_function=self.cam_client.get_thresh))
        return layout

    



import os
import time
import kivy
from kivy.config import Config
from kivy.app import App
from kivy.uix import camera
Config.set(
    'kivy',
    'default_font',
    ['TmonBlack', './TTF/TMONBlack.ttf', None, './TTF/TMONBlack.ttf', None]
    )
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup


class Upper_bar(BoxLayout):
    pass

class Under_bar(BoxLayout): #아이디 하나 만들기
    pass

class box(App):
    Save_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    def capture(self):
        camera = self.root.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")

class LocationPop(Popup):
    def __init__(self, **kwargs):
        super(LocationPop, self).__init__(**kwargs) #본인창 불러오기
        self.ids['filechooser'].path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')


if __name__ == '__main__':
    box().run()

class CameraClick(BoxLayout):
    pass

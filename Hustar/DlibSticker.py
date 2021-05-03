#-*- coding:utf-8 -*-
import kivy
from kivy.config import Config

Config.set(
    'kivy',
    'default_font',
    ['TmonBlack', './TTF/TMONBlack.ttf', None, './TTF/TMONBlack.ttf', None]
)

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.clock import Clock

import cmake
import dlib
import cv2
import os
import time

import threading

predictor_path = 'shape_predictor_68_face_landmarks.dat'
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)


class Upper_bar(BoxLayout):
    pass



class MyCamera(Image):
    thread = ''
    capture = ''
    opencvImage = ''

    def __init__(self, **kwagrs):
        super(MyCamera, self).__init__(**kwagrs)
        print('I\'m Init.')
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            print("Camera Error")

        self.fps = self.capture.get(cv2.CAP_PROP_FPS)
        print(self.fps)
        # while True:
        #     self.update(0)

        # self.thread.start()

    def threadStart(self):
        print('Thread Start')
        self.thread = threading.Thread(target=self.update)
        self.thread.start()

    def update(self, dt):
        #print('update')
        # while True:
        ret, frame = self.capture.read()
        if ret:
            # buf1 = cv2.flip(frame, 0)
            buf1 = frame
            # buf1 = cv2.flip(frame, -1)

            gray = cv2.cvtColor(buf1, cv2.COLOR_BGR2GRAY)
            # gray = buf1
            dets = detector(gray, 0)
            for k, d in enumerate(dets):
                # print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                #     k, d.left(), d.top(), d.right(), d.bottom()))
                # Get the landmarks/parts for the face in box d.
                shape = predictor(gray, d)

                for count in range(0, 68):
                    a = str(shape.part(count))
                    a = a.replace('(', '')
                    a = a.replace(')', '')
                    xPoint, yPoint = a.split(',')

                    cv2.circle(buf1, (int(xPoint), int(yPoint)), 1, (255, 255, 0), -1)
                #             print(count)
                #             print(f'{shape.part(count)}')


            # 좌우 반전.
            buf1 = cv2.flip(buf1, 1)

            # 상하 반전.
            buf1 = cv2.flip(buf1, 0)
            self.openCVImage = buf1


            buf = buf1.tobytes()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr'
            )
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = image_texture

class LocationPop(Popup):
    def __init__(self, **kwargs):
        super(LocationPop, self).__init__(**kwargs)
        self.ids['filechooser'].path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

class DlibSticker(App):
    Save_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    prefixFileName = '\\HuNow_'
    print(prefixFileName)

    def imageSave(self, **kwargs):
        currentTime = time.strftime("%Y%m%d_%H%M%S")
        cv2.imwrite(f'{self.Save_path}{self.prefixFileName}{currentTime}.png',
                    self.root.ids['camera'].openCVImage)

    def printOpenImage(self, **kwargs):
        currentTime = time.strftime("%Y%m%d_%H%M%S")
        print('openImage', f'{self.Save_path}{self.prefixFileName}{currentTime}.png')

    def on_start(self, **kwargs):
        print('first start')
        Clock.schedule_interval(self.root.ids['camera'].update, 1.0 / 33.0)


if __name__ == '__main__':
    mainApp = DlibSticker()
    mainApp.run()
import kivy
from kivy.config import Config

Config.set(
    'kivy',
    'default_font',
    ['HangeulNuri', './TTF/HangeulNuriR.ttf', None, './TTF/HangeulNuriB.ttf', None]
    )

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.clock import Clock
import numpy as np
import math

def myImwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)
        if result:
            with open(filename, mode='w+b') as f:
                 n.tofile(f)
            return True
        else:
            return False

    except Exception as e:
        print(e)
        return False

def overlay_image_alpha(img, img_overlay, x, y, alpha_mask):
    """Overlay `img_overlay` onto `img` at (x, y) and blend using `alpha_mask`.

    `alpha_mask` must have same HxW as `img_overlay` and values in range [0, 1].
    """

    # Image ranges
    y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

    # Overlay ranges
    y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
    x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

    # Exit if nothing to do
    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return

    # Blend overlay within the determined ranges
    img_crop = img[y1:y2, x1:x2]
    img_overlay_crop = img_overlay[y1o:y2o, x1o:x2o]
    alpha = alpha_mask[y1o:y2o, x1o:x2o, np.newaxis]
    alpha_inv = 1.0 - alpha

    img_crop[:] = alpha * img_overlay_crop + alpha_inv * img_crop

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

class Under_bar(BoxLayout):
    pass


class MyCamera(Image):

    thread = ''
    capture = ''
    opencvImage = ''
    faceDict = dict()
    stickerImage = cv2.imread(f'./sticker/tear.png', cv2.IMREAD_UNCHANGED)

    def __init__(self, **kwagrs):
        super(MyCamera, self).__init__(**kwagrs)
        print('I\'m Init.')
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            print("Camera Error")

        self.fps = self.capture.get(cv2.CAP_PROP_FPS)
        print(self.fps)


    def setSticker(self, file_name='tear.png'):
        self.stickerImage = cv2.imread(f'./sticker/{file_name}', cv2.IMREAD_UNCHANGED)



    def update(self, dt):
        countNumber = 0
        padding = 25
        ret, frame = self.capture.read()
        if ret:
            # buf1 = cv2.flip(frame, 0)
            buf1 = frame
            # buf1 = cv2.flip(frame, -1)

            gray = cv2.cvtColor(buf1, cv2.COLOR_BGR2GRAY)
            # gray = buf1
            dets = detector(gray, 0)

            for k, d in enumerate(dets):

                print(d.left(), d.top(), d.right(), d.bottom())



                # print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                #     k, d.left(), d.top(), d.right(), d.bottom()))
                # Get the landmarks/parts for the face in box d.
                shape = predictor(gray, d)

                start1 = (shape.part(0).x-padding, shape.part(19).y-padding)
                end1 = (shape.part(16).x+padding, shape.part(8).y+padding)
                start2 = (shape.part(0).x-padding, shape.part(24).y-padding)
                end2 = (shape.part(16).x+padding, shape.part(8).y+padding)
                r_pos = [0, 0] # 사각형 좌표 접근을 위한 변수
                if (shape.part(19).y <= shape.part(24).y):
                    cv2.rectangle(buf1, start1, end1, (255, 0, 0), 2)
                    self.faceDict[f'{countNumber}'] = buf1[shape.part(19).y-padding:shape.part(8).y+padding, shape.part(0).x-padding:shape.part(16).x+padding]
                    r_pos = [start1, end1]

                else:
                    cv2.rectangle(buf1, start2, end2, (0, 255, 0), 2)
                    self.faceDict[f'{countNumber}'] = buf1[shape.part(24).y-padding:shape.part(8).y+padding, shape.part(0).x-padding:shape.part(16).x+padding]
                    r_pos = [start2, end2]


                for count in range(0,68):
                    cv2.circle(buf1, (shape.part(count).x, shape.part(count).y), 1, (255,255,0), -1)
                    break


                height = shape.part(0).y - shape.part(16).y
                # print('height', height)
                slide = math.sqrt(math.pow(shape.part(0).x - shape.part(16).x, 2.0) + math.pow(shape.part(0).y - shape.part(16).y, 2.0))
                # print('slide', slide)
                radian = math.asin(height/slide)
                degree = math.degrees(radian)
                # print('degree', degree)

                faceHeight, faceWidth = self.faceDict[f'{countNumber}'].shape[:2]

                try:
                    # pivot = (faceHeight/2, faceWidth/2)
                    # stickerResize = cv2.resize(self.stickerImage, self.faceDict[f'{countNumber}'].shape[:2])
                    # stickerMatrix = cv2.getRotationMatrix2D(pivot, degree, 1.0)
                    # testAffine = cv2.warpAffine(stickerResize, stickerMatrix, self.faceDict[f'{countNumber}'].shape[:2])
                    # image_overlay = testAffine[:, :, :3]
                    # alpha_mask = testAffine[:, :, 3] / 255.0
                    # # cv2.imshow('testAffine', testAffine)
                    
                    rows, cols = self.stickerImage.shape[:2]
                    # 원근 변환 전 4개 좌표
                    pts1 = np.float32([[0,0], [0,rows], [cols, 0], [cols,rows]])
                    # 원근 변환 후 4개 좌표
                    pts2 = np.float32([
                        [50, shape.part(17).y - shape.part(26).y + 50], 
                        [shape.part(4).x - shape.part(17).x + 50, shape.part(4).y - shape.part(26).y + 50], 
                        [shape.part(26).x - shape.part(17).x + 50, 50], 
                        [shape.part(12).x - shape.part(17).x + 50, shape.part(12).y - shape.part(26).y + 50]
                    ])

                    # 원근 변환 행렬 계산
                    mtrx = cv2.getPerspectiveTransform(pts1, pts2)
                    # 원근 변환 적용
                    dst = cv2.warpPerspective(self.stickerImage, mtrx, (cols, rows))
                    cv2.imshow('perspective', dst)

                    # 스티커 이미지 포지션 조절
                    s_pos = [shape.part(17).x, shape.part(17).y]
                    if shape.part(17).y > shape.part(26).y :
                        s_pos[1] = shape.part(26).y
                    else: # 이게 왜 되노;;ㅣ
                        s_pos[1] = s_pos[1] + (shape.part(26).y - shape.part(17).y)

                    overlay_image_alpha(buf1, dst[:, :, :3], s_pos[0] - 50, s_pos[1] - 50, dst[:, :, 3] / 255.0)
                except:
                    print('rotate Error')


                countNumber += 1


            for (k, v) in self.faceDict.items():
                try:
                    cv2.imshow(f'{k} Key', v)

                except:
                    print("Exception")
            # 좌우 반전.
            buf1 = cv2.flip(buf1, 1)
            self.openCVImage = buf1

            # 상하 반전.
            buf1 = cv2.flip(buf1, 0)


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


class TestKivy(App):
    Save_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    prefixFileName = '\\HuNow_'
    print(prefixFileName)



    def imageSave(self, **kwargs):
        currentTime = time.strftime("%Y%m%d_%H%M%S")
        myImwrite(f'{self.Save_path}{self.prefixFileName}{currentTime}.png',
            self.root.ids['camera'].openCVImage)

    def printOpenImage(self, **kwargs):
        currentTime = time.strftime("%Y%m%d_%H%M%S")
        print('openImage',f'{self.Save_path}{self.prefixFileName}{currentTime}.png')


    def on_start(self, **kwargs):
        print('first start')
        Clock.schedule_interval(self.root.ids['camera'].update, 1.0/33.0)


if __name__ == '__main__':
    mainApp = TestKivy()
    mainApp.run()

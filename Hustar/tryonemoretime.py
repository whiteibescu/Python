#!/usr/bin/python
# The contents of this file are in the public domain. See LICENSE_FOR_EXAMPLE_PROGRAMS.txt
#
#   This example program shows how to find frontal human faces in an image and
#   estimate their pose.  The pose takes the form of 68 landmarks.  These are
#   points on the face such as the corners of the mouth, along the eyebrows, on
#   the eyes, and so forth.
#
#   The face detector we use is made using the classic Histogram of Oriented
#   Gradients (HOG) feature combined with a linear classifier, an image pyramid,
#   and sliding window detection scheme.  The pose estimator was created by
#   using dlib's implementation of the paper:
#      One Millisecond Face Alignment with an Ensemble of Regression Trees by
#      Vahid Kazemi and Josephine Sullivan, CVPR 2014
#   and was trained on the iBUG 300-W face landmark dataset (see
#   https://ibug.doc.ic.ac.uk/resources/facial-point-annotations/):
#      C. Sagonas, E. Antonakos, G, Tzimiropoulos, S. Zafeiriou, M. Pantic.
#      300 faces In-the-wild challenge: Database and results.
#      Image and Vision Computing (IMAVIS), Special Issue on Facial Landmark Localisation "In-The-Wild". 2016.
#   You can get the trained model file from:
#   http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2.
#   Note that the license for the iBUG 300-W dataset excludes commercial use.
#   So you should contact Imperial College London to find out if it's OK for
#   you to use this model file in a commercial product.
#
#
#   Also, note that you can train your own models using dlib's machine learning
#   tools. See train_shape_predictor.py to see an example.
#
#
# COMPILING/INSTALLING THE DLIB PYTHON INTERFACE
#   You can install dlib using the command:
#       pip install dlib
#
#   Alternatively, if you want to compile dlib yourself then go into the dlib
#   root folder and run:
#       python setup.py install
#
#   Compiling dlib should work on any operating system so long as you have
#   CMake installed.  On Ubuntu, this can be done easily by running the
#   command:
#       sudo apt-get install cmake
#
#   Also note that this example requires Numpy which can be installed
#   via the command:
#       pip install numpy

import sys
import os
import dlib
import glob
import cv2
import numpy as np


# 투명한 이미지 overlay하는 함수
def transparentOverlay(src, overlay, pos=(0, 0), scale=1):
    """
    :param src: Input Color Background Image
    :param overlay: transparent Image (BGRA)
    :param pos:  position where the image to be blit.
    :param scale : scale factor of transparent image.
    :return: Resultant Image
    """
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w, _ = overlay.shape  # Size of foreground
    rows, cols, _ = src.shape  # Size of background Image
    y, x = pos[0], pos[1]  # Position of foreground/overlay image

    # loop over all pixels and apply the blending equation
    for i in range(h):
        for j in range(w):
            if x + i >= rows or y + j >= cols:
                continue
            alpha = float(overlay[i][j][3] / 255.0)  # read the alpha channel
            src[x + i][y + j] = alpha * overlay[i][j][:3] + (1 - alpha) * src[x + i][y + j]
    return src


############################################################################

if len(sys.argv) != 1:
    print(
        "Give the path to the trained shape predictor model as the first "
        "argument and then the directory containing the facial images.\n"
        "For example, if you are in the python_examples folder then "
        "execute this program by running:\n"
        "    ./face_landmark_detection.py shape_predictor_68_face_landmarks.dat ../examples/faces\n"
        "You can download a trained facial shape predictor from:\n"
        "    http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
    exit()

predictor_path = 'shape_predictor_68_face_landmarks.dat'
faces_folder_path = 'face'

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

cap = cv2.VideoCapture(0)

if not cap.isOpened:
    print('Camera load failed!')

print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(cap.get(cv2.CAP_PROP_FPS))

sticker = cv2.imread("./sticker/cat.png", cv2.IMREAD_UNCHANGED)  # 스티커 이미지
rows, cols = sticker.shape[:2]
# 원근 변환 전 4개 좌표
pts1 = np.float32([[0, 0], [0, rows], [cols, 0], [cols, rows]])

# while True:
while True:
    ret, frame = cap.read()

    img = frame

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    dets = detector(gray, 0)

    for k, d in enumerate(dets):
        # print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
        #     k, d.left(), d.top(), d.right(), d.bottom()))
        # Get the landmarks/parts for the face in box d.
        shape = predictor(gray, d)

        for count in range(0, 68):
            fpoint = shape.part(count)

            cv2.circle(img, (fpoint.x, fpoint.y), 1, (255, 255, 0), -1)

            #             print(count)
            #             print(f'{shape.part(count)}')

        # 원근 변환 후 4개 좌표
        pts2 = np.float32([[shape.part(17).x, shape.part(17).y], [shape.part(5).x, shape.part(5).y],
                           [shape.part(26).x, shape.part(26).y], [shape.part(11).x, shape.part(11).y]])
        # 원근 변환 행렬 계산
        mtrx = cv2.getPerspectiveTransform(pts1, pts2)
        # 원근 변환 적용
        dst = cv2.warpPerspective(sticker, mtrx, (cols, rows))
        cv2.imshow('perspective', dst)

        img = transparentOverlay(img, dst, (0, 0), 1)

    cv2.imshow("origin", sticker)

    cv2.imshow("test", img)

    if cv2.waitKey(int(1000 / 30)) & 0xFF == ord('q'):
        break

    # for count in range(0,68):
    #
    #     print(count)
    #     print(f'{shape.part(count)}')

cap.release()

# for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
#     print("Processing file: {}".format(f))
#     img = dlib.load_rgb_image(f)
#     print(img)
#     cv2.waitKey()
#     win.clear_overlay()
#     win.set_image(img)
#
#     # Ask the detector to find the bounding boxes of each face. The 1 in the
#     # second argument indicates that we should upsample the image 1 time. This
#     # will make everything bigger and allow us to detect more faces.
#     dets = detector(img, 1)
#     print('dets:', dets)
#     print("Number of faces detected: {}".format(len(dets)))
#     for k, d in enumerate(dets):
#         print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
#             k, d.left(), d.top(), d.right(), d.bottom()))
#         # Get the landmarks/parts for the face in box d.
#         shape = predictor(img, d)
#
#
#         print("Part 0: {}, Part 1: {} ...".format(shape.part(0),
#                                                   shape.part(1)))
#
#         for count in range(0,68):
#             print(count)
#             print(f'{shape.part(count)}')

# Draw the face landmarks on the screen.
# win.add_overlay(shape)

# win.add_overlay(dets)
# dlib.hit_enter_to_continue()
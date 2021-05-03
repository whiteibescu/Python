import sys
import os
import dlib
import glob
import cv2



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

        for count in range(0,68):

            a = str(shape.part(count))
            a = a.replace('(', '')
            a = a.replace(')', '')
            xPoint, yPoint = a.split(',')

            cv2.circle(img, (int(xPoint), int(yPoint)), 1, (255,255,0), -1)
        #             print(count)
        #             print(f'{shape.part(count)}')

    cv2.imshow("test", img)

    if cv2.waitKey(int(1000/30)) & 0xFF == ord('q'):
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
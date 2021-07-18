# smarthome module
import RPi.GPIO as GPIO
from time import sleep

# flask module
from flask import Flask

# AI module
import numpy as np
import cv2
import pickle
import threading


# Face Detaction Threading

# if display error:
# export DISPLAY=:0.0
# xhost +local:root
# xhost +localhost

is_Obama = 0

def faceDetact():
    global is_Obama

    face_cascade = cv2.CascadeClassifier('../../OpenCV-Python-Series/src/cascades/data/haarcascade_frontalface_alt2.xml')
    # eye_cascade = cv2.CascadeClassifier('../../OpenCV-Python-Series/src/cascades/data/haarcascade_eye.xml')
    # smile_cascade = cv2.CascadeClassifier('../../OpenCV-Python-Series/src/cascades/data/haarcascade_smile.xml')


    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("../../OpenCV-Python-Series/src/recognizers/face-trainner.yml")

    labels = {"person_name": 1}
    with open("../../OpenCV-Python-Series/src/pickles/face-labels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v:k for k,v in og_labels.items()}

    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            #print(x,y,w,h)
            roi_gray = gray[y:y+h, x:x+w] #(ycord_start, ycord_end)
            roi_color = frame[y:y+h, x:x+w]

            # recognize? deep learned model predict keras tensorflow pytorch scikit learn
            id_, conf = recognizer.predict(roi_gray)
            if conf>=4 and conf <= 85:
                #print(5: #id_)
                #print(labels[id_])
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (255, 255, 255)
                stroke = 2
                cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                
                # added code
                if name != 'obama':
                    is_Obama = 0
                else:
                    is_Obama = 1
                # added code - end

            img_item = "7.png"
            cv2.imwrite(img_item, roi_color)

            color = (255, 0, 0) #BGR 0-255 
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
            #subitems = smile_cascade.detectMultiScale(roi_gray)
            #for (ex,ey,ew,eh) in subitems:
            #   cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

global t
t = threading.Thread(target=faceDetact)
t.daemon = True
t.start()


# main - flask w/ NLP

app = Flask(__name__)

LED_1 = 4
LED_2 = 5
LED_3 = 14
LED_4 = 15
LEDs = [LED_1, LED_2, LED_4, LED_3]

FAN = [18, 27]

is_on = [False]

@app.route('/')
def hello():
    return "hello world"

@app.route('/ledone/<ledonoff>/<ledNum>')
def oneLed(ledonoff, ledNum):
    if ledonoff == "on":
        status = True
    if ledonoff == "off":
        status = False
        
    for idx, LED in enumerate(LEDs):
        if ledNum == str(idx+1):
            if is_Obama == 1:
                GPIO.output(LED, status)
                print(f"led {ledNum} {ledonoff}")
    return "led one"

@app.route('/fan/<time>')
def fanonoff(time):
    if not time.isdigit():
        return "Failed to fan on"
    
    time = int(time)
    
    if time not in (1, 2, 3):
        return "Failed to fan on"
    
    print(f"FAN Turn on for {time} seconds")
    GPIO.output(18,1)
    GPIO.output(27,0)
    sleep(time)
    GPIO.output(18,0)
    GPIO.output(27,0)
    return "FAN on"

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LEDs, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(FAN, GPIO.OUT, initial=GPIO.LOW)
    app.run(host='0.0.0.0', port=5000, debug=False)


if __name__ == "__main__":
    main()
        

import RPi.GPIO as GPIO
from time import sleep

from flask import Flask
app = Flask(__name__)

LED_1 = 4
LED_2 = 5
LED_3 = 14
LED_4 = 15
LEDs = [LED_1, LED_2, LED_4, LED_3]
is_on = [False]

@app.route('/')
def hello():
    return "hello world"

@app.route('/led/<onoff>')
def ledonoff(onoff):
    if onoff == "on":
        print("LED Turn on")
        GPIO.output(LEDs, 1)
        is_on[0] = True
        return "LED on"

    elif onoff == "off":
        print("LED Turn off")
        GPIO.output(LEDs, 0)
        return "LED off"

    elif onoff == "party":
        if is_on[0]:
            print("Activate Party Mode")
            for _ in range(5):
                GPIO.output(LEDs, 0)
                sleep(0.5)
                GPIO.output(LEDs, 1)
                sleep(0.5)
            return "Party on"
        return "Turn on LED first"

@app.route('/ledone/<ledonoff>/<ledNum>')
def ledoff(ledonoff, ledNum):
    if ledonoff == "on":
        status = True
    if ledonoff == "off":
        status = False
        
    for idx, LED in enumerate(LEDs):
        if ledNum == str(idx+1):
            GPIO.output(LED, status)
            print(f"led {idx+1} off")
    return "led one"


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LEDs, GPIO.OUT, initial=GPIO.LOW)
    app.run(host='0.0.0.0', port=5000, debug=True)

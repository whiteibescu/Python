import RPi.GPIO as GPIO
from time import sleep

LED_1 = 4
LED_2 = 5
LED_3 = 14
LED_4 = 15
LEDs = [LED_1, LED_2, LED_3, LED_4]


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LEDs, GPIO.OUT, initial=False)
    print('main() program running...')

    try:
        while True:
            for LED in LEDs:
                GPIO.output(LED, GPIO.HIGH)
                sleep(0.5)

            for LED in LEDs[::-1]:
                GPIO.output(LED, GPIO.LOW)
                sleep(0.5)

    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
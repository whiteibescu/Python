import RPi.GPIO as GPIO
from time import sleep
import spidev

spi = spidev.SpiDev()
CDS_CHANNEL = 0

LED_1 = 4
LED_2 = 5
LED_3 = 14
LED_4 = 15
LEDs = [LED_1, LED_2, LED_3, LED_4]

def initMcp3208():
    spi.open(0, 0)
    spi.max_speed_hz = 1000000
    spi.mode = 3

def buildReadCommand(channel):
    startBit = 0x04
    singleEnded = 0x08

    configBit = [startBit | ((singleEnded | (channel & 0x07)) >> 2), (channel & 0x07) << 6, 0x00]

    return configBit

def processAdcValue(result):
    byte2 = (result[1] & 0x0F)
    return (byte2 << 8 | result[2])
    
def analogRead(channel):
    if (channel > 7) or (channel < 0):
        return -1

    r = spi.xfer2(buildReadCommand(channel))
    adc_out = processAdcValue(r)
    return adc_out

def controlMcp3208(channel):
    analogVal = analogRead(channel)
    return analogVal

def readSensor(channel):
    return controlMcp3208(channel)

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LEDs, GPIO.OUT, initial = False)
    initMcp3208()
    print("Setup pin as outputs")

    try:
        while True:
            readVal = readSensor(CDS_CHANNEL)

            voltage = readVal * 4.096 / 4096
            
            if voltage < 1:
                GPIO.output(LEDs, GPIO.HIGH)
            elif 1 <= voltage and voltage < 2:
                GPIO.output(LEDs[0:3], GPIO.HIGH)
                GPIO.output(LEDs[3:], GPIO.LOW)
            elif 2 <= voltage and voltage < 3:
                GPIO.output(LEDs[0:2], GPIO.HIGH)
                GPIO.output(LEDs[2:], GPIO.LOW)
            elif 3 <= voltage and voltage < 3.5:
                GPIO.output(LEDs[0], GPIO.HIGH)
                GPIO.output(LEDs[1:], GPIO.LOW)
            elif 3.5 <= voltage:
                GPIO.output(LEDs, GPIO.LOW)
                

            print(f"CDS Val={readVal}\tVoltage={voltage}")
            sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()
        spi.close()

if __name__ == '__main__':
    main()

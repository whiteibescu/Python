import board
import adafruit_dht
from time import sleep

dhtDevice = adafruit_dht.DHT11(board.D17)

def main():
    print("main() program")
    while True:
        try:
            temperature_c = dhtDevice.temperature
            humidity = dhtDevice.humidity
            print(f"Temp: {temperature_c:.1f} Humidity: {humidity}")
        except RuntimeError as error:
            print(error.args[0])
        sleep(2.0)

if __name__ == '__main__':
    main()
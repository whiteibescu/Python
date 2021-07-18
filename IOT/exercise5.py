import board
import adafruit_dht
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd
import GPIO_EX
from time import sleep

# DHT11
dhtDevice = adafruit_dht.DHT11(board.D17)

# LCD
lcd_rs = digitalio.DigitalInOut(board.D22)
lcd_en = digitalio.DigitalInOut(board.D24)
lcd_d7 = digitalio.DigitalInOut(board.D21)
lcd_d6 = digitalio.DigitalInOut(board.D26)
lcd_d5 = digitalio.DigitalInOut(board.D20)
lcd_d4 = digitalio.DigitalInOut(board.D19)

lcd_columns = 16
lcd_rows = 2

lcd = character_lcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

def initTextlcd():
    lcd.clear()
    lcd.home()
    lcd.cursor_position(0, 0)
    sleep(1.0)

def displayText(text=' ', col=0, row=0):
    lcd.cursor_position(col, row)
    lcd.message = text

def clearTextlcd():
    lcd.clear()
    lcd.message = 'clear LCD\nGoodbye!'
    sleep(2.0)
    lcd.clear()

# Keypad

ROW0_PIN = 0
ROW1_PIN = 1
ROW2_PIN = 2
ROW3_PIN = 3
COL0_PIN = 4
COL1_PIN = 5
COL2_PIN = 6

COL_NUM = 3
ROW_NUM = 4

g_preData = 0

colTable = [COL0_PIN, COL1_PIN, COL2_PIN]
rowTable = [ROW0_PIN, ROW1_PIN, ROW2_PIN, ROW3_PIN]

rowData = [n for n in range(ROW_NUM)]

def initKeypad():
    for i in range(0, COL_NUM):
        GPIO_EX.setup(colTable[i], GPIO_EX.IN)
    for i in range(0, ROW_NUM):
        GPIO_EX.setup(rowTable[i], GPIO_EX.OUT)
        
def selectRow(rowNum):
    for i in range(0, ROW_NUM):
        if rowNum == (i + 1):
            GPIO_EX.output(rowTable[i], GPIO_EX.HIGH)
            sleep(0.001)
        else:
            GPIO_EX.output(rowTable[i], GPIO_EX.LOW)
            sleep(0.001)
    return rowNum

def readCol():
    keypadstate = -1
    for i in range(0, COL_NUM):
        inputKey = GPIO_EX.input(colTable[i])
        if inputKey:
            keypadstate = keypadstate + (i + 2)
            sleep(0.5)
    return keypadstate

def readKeypad():
    global g_preData
    keyData = -1
    
    runningStep = selectRow(1)
    rowData[0] = readCol()
    selectRow(0)
    sleep(0.001)
    if (rowData[0] != -1):
        keyData = rowData[0]
                
    for i in range(1, ROW_NUM):
        if runningStep == i:
            if keyData == -1:
                runningStep = selectRow(i+1)
                rowData[i] = readCol()
                selectRow(0)
                sleep(0.001)
                if rowData[i] != -1:
                    if i == 3:
                        if rowData[i] == 1:
                            keyData = '*'
                        elif rowData[i] == 2:
                            keyData = 0
                        elif rowData[i] == 3:
                            keyData = '#'
                    else:
                        keyData = rowData[i] + (3 * i)
                
                
    sleep(0.1)
    
    if keyData == -1:
        return -1
    
    if g_preData == keyData:
        g_preData = -1
        return -1
    g_preData = keyData
    
    print(f"\r\nKeypad Data : {keyData}")
    
    return keyData

# main

password = []
password_chk = []

def main():
    initTextlcd()
    print("main() program")

    while True:
        try:
            lcd.clear()
            temperature_c = dhtDevice.temperature
            humidity = dhtDevice.humidity
            
            line = f"Temp. {temperature_c:.1f} C\nHumidity {humidity} %"
            displayText(line, 0, 0)
            
            sleep(3)

        except KeyboardInterrupt:
            clearTextlcd()

if __name__ == '__main__':
    main()
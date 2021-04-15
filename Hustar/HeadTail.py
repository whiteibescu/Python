import random

myList = ["head", "tail"]

while True:
    response = input("동전 던지기를 던지겠습니까? (yes, no)")
    if response == "yes":
        coin = random.choice(myList)
        print(coin)
    else:
        break
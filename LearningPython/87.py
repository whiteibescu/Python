import random
hanguls = list("가나달마바사아자카타파하")

with open("info.txt", "w") as file:
    for i in range(1000):
        name = random.choice(hanguls) + random.choice(hanguls)
        weight = random.randrange(40, 100)
        height = random.randrage(140, 200)

        file.write("{}, {} {}\n".format(name, weight, height))
import os

print("현재 운영체제:", os.name)
print("현재 폴더:", os.getcwd())
print("현재 폴더 내부의 요소:", os.listdir())

os.mksir("hello")
os.rmdir("hello")

with open("original.txt", "w") as file:
    file.write("hello")
os.rename("original.txt", "new.txt")

os.remove("new.txt")

os.system("dir")


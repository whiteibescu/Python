import os.path

# 메인함수 (show(), command 받기)
def main():
    # 평균과 학점계산해서 sDict에 저장
    command = input("# ").lower()

    if command == 'show':
        show(sDict)
    elif command == 'search':
        search(sDict)
    elif command == 'changescore':
        changescore(sDict)
    elif command == 'add':
        rawDict = add(sDict)
        return rawDict
    elif command == 'searchgrade':
        searchgrade(sDict)
    elif command == 'remove':
        rawDict = remove(sDict)
        return rawDict
    elif command == 'quit':
        quit(sDict)

# 부가적인 함수

def setting():
    # student 표의 머릿말 부분
    print(index)
    print(dot)
def stu(id,sDict):
    # student id와 딕셔너리를 넣으면 한줄로 values를 예쁘게 뽑아줌
    id = str(id)
    # print(id, sDict[id][0], sDict[id][1],sDict[id][2],sDict[id][3],sDict[id][4], sep='\t')
    print("%s %18s %10s %10s %10s %10s"%(id, sDict[id][0], sDict[id][1],sDict[id][2],sDict[id][3],sDict[id][4]))

def dictsave(rawDict):
    # 평균과 학점을 딕셔너리로 저장
    sDict = {}
    for stuID in rawDict:
        li = rawDict[stuID][:]
        avg = (float(li[1])+float(li[2]))/2
        if avg >= 90:
            grade = 'A'
        elif avg >= 80:
            grade = 'B'
        elif avg >= 70:
            grade = 'C'
        elif avg >= 60:
            grade = 'D'
        else:
            grade = 'F'
        li.append(avg) ; li.append(grade)
        sDict[stuID] = list(map(str, li))
    return sDict


# 7개의 함수
def show(sDict):
    setting()
    sortsDict = sorted(sDict.items(), key=lambda x: x[1][3], reverse=True)
    for i in sortsDict:
        stu(i[0], sDict)

def search(sDict):
    id = input('Student ID: ')
    if id in sDict:
        setting()
        stu(id,sDict)
    else:
        print("NO SUCH PERSON")

def changescore(sDict):
    id = input("Student ID: ")
    if id in sDict:
        term = input("Mid/Final?").lower()
        if term == 'mid':
            newScore = int(input("Input new score: "))
            if 0<= newScore <=100 :
                setting()
                stu(id,sDict)
                rawDict[id][1] = newScore
                sDict = dictsave(rawDict)
                print('Score changed.')
                stu(id, sDict)
                return rawDict
        elif term == 'final':
            newScore = int(input("Input new score: "))
            if 0 <= newScore <= 100 :
                setting()
                stu(id,sDict)
                rawDict[id][2] = newScore
                sDict = dictsave(rawDict)
                print('Score changed.')
                stu(id, sDict)
                return rawDict
    else:
        print("NO SUCH PERSON")


def add(sDict):
    stuId = input("Student ID: ")
    if stuId in rawDict:
        print("ALREADY EXIST")
        main()
    else :
        name = input("Name: ")
        mid = input("Midterm Score: ")
        final = input("Final Score: ")
        rawDict[stuId] = [name, mid, final]
        print("Student added.")
    return rawDict


def searchgrade(sDict):
    grade = input("Grade to search: ")
    if grade in ('A','B','C','D','F'):
        count = 0
        li = []
        for i in sDict:
            if sDict[i][-1] == grade:
                li.append(i)
                count += 1
        if count == 0:
            print("NO REUSLTS")
        else:
            setting()
            for i in li:
                stu(i,sDict)

def remove(sDict):
    if sDict == {}:
        print("List is empty.")
    else:
        id = input("Student ID: ")
        if id not in sDict:
            print("NO SUCH PERSON.")
        else:
            del rawDict[id]
            print("Student removed.")
    return rawDict

def quit(sDict):
    yesno = input('Save data?[yes/no]').lower()
    if yesno == 'yes':
        filename = input('File name : ')
        newfile = open(filename, 'w')
        for id in sDict:
            line = id + '\t' + sDict[id][0] + '\t' + sDict[id][1] + '\t' + sDict[id][2] +'\n'
            newfile.write(line)
        newfile.close()
    file.close()
    sys.exit()


# 프로그램시작(파일열기, 파일을 간단한 딕셔너리로 저장, 필요한 변수 선언)
if __name__ == '__main__':
    # 라이브러리 import
    import sys
    # 파일열기
    try:
        file = open(sys.argv[1], 'r')
    except:
        file = open("students.txt", 'r')

    # rawDict에 저장
    rawDict = {}
    for line in file:
        li = []
        li = line.strip().split('\t')
        id = li.pop(0)
        rawDict[id] = li
    # 평균과 학점계산해서 sDict에 저장
    sDict = dictsave(rawDict)
    # 변수선언
    index = ' Student             Name       Midterm     Final     Average      Grade'
    dot = '--------------------------------------------------------------------------'
    # show,main 함수 호출
    show(sDict)
    while True:
        main()
        sDict = dictsave(rawDict)
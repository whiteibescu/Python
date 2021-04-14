STUDENTS = 5
scores = []
scoresSum = 0

for i in range(STUDENTS):
    value = int(input("성적을 입력하세요 "))
    scores.append(value)
    scoresSum += value  # 단축 연산자

scoreAvg = scoresSum / len(scores)
highScoreStudents = 0
for i in range(len(scores)):
    if scores[i] >= 80:
        highScoreStudents += 1

print("성적 평균은", scores)
print("80점 이상 성적을 받은 학생은", highScoreStudents)

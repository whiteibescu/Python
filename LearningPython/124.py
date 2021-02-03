class CustomException(Exception):
    def __init__(self):
        Exception.__init__(self)
        print("#### 내가 만든 오류가 생성되었습니다! ####")
    def __str__(self):
        return "오류가 발생했어요"

raise CustomException

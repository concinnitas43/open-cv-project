import cv2

snack_list = []
snack_points = [0 for i in range(len(snack_list))]
thresh_point = 100

def where_snack(frame):  # 스낵의 존재성 판별 
    is_there_snack = False 
    snack_location = []  # snack 위치 roi 
    return is_there_snack, snack_location 

def which_snack(roi):  # 스낵 roi 값이 주어졌을 때 어떤거인지 판별
    return 0  # 스낵리스트에서의 인덱스 리턴

def tts(name): #이름 말하기
    pass 

def run():
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        while True:
            ret, frame = cap.read()
            if ret:
                is_there_snack, snack_location = where_snack(frame)  # 스낵이 있는지, 어느 위치에 있는지 판별
                if is_there_snack:  # 스낵이 있으면
                    snack_number = which_snack(snack_location)  # 스낵 위치 받아서 분석
                    snack_points[snack_number] += 1  # 분석하면 여러가지 과자 후보군이 나올텐데 한 종류의 과자가 탐지되면 감지된 시간에 따라 거기에 점수를 더하기
                    if max(snack_points)==thresh_point:  # 더해진 점수 값이 특정 지점에 도달하면(=어느정도의 시간동안 감지되면)
                        tts(snack_list)  # tts로 음성 출력
                        break
            else:
                print("no frame")
                break
    else:
        print("can't open camera")

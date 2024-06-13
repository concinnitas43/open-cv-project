import cv2

is_there_snack = False

attempt = 90 # 혹시라도 겹치지 않게 하기 위해서 시도 횟수 정의

snack_no = 6 # 간식 번호

# 카메라 열기
cap = cv2.VideoCapture(0)
if cap.isOpened():
    frame_no = 0
    while True:
        ret, frame = cap.read() # 카메라에서 프레임 읽기

        # frame = cv2.flip(frame, 1)

        x = cv2.waitKey(1)

        if x == ord(" "): # 화면에 과자가 있는건지 없는건지 전환 
            is_there_snack = not is_there_snack
            attempt += 1

        if x == ord("q"): # 멈추기 
            break

        if ret:
            frame_no += 1 # 프레임 번호 따로따로 부려하기 위해서 
            if is_there_snack:
                save_name = f'./snack_data/snack{snack_no}/'+'img_'+str(is_there_snack)+'_'+str(attempt)+'_'+str(frame_no)+'.jpg'
                cv2.imwrite(save_name, frame) # 프레임을과자 데이터에 저장
                frame = cv2.rectangle(frame, (0, 0), (50, 50), (0, 255, 0), 2) # 과자가 있어야 한다는 것을 화면에 초록색 상자로 표시
                cv2.imshow('img', frame)
            else:
                save_name = './snack_data/snack0/'+'img_'+str(is_there_snack)+'_'+str(attempt)+'_'+str(frame_no)+'.jpg'
                cv2.imwrite(save_name, frame) # 프레임을 공백 데이터에 저장 
                frame = cv2.rectangle(frame, (0, 0), (50, 50), (0, 0, 255), 2) # 과자가 없어야 한다는 것을 화면에 빨간색 상자로 표시ㅣ 
                cv2.imshow('img', frame)
        else:
            print('no frame')
else:
    print("can't open camera")


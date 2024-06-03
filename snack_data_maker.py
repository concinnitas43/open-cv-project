import cv2

is_there_snack = False
attempt = 1

snack_no = 2

cap = cv2.VideoCapture(0)
if cap.isOpened():
    frame_no = 0
    while True:
        ret, frame = cap.read()

        frame = cv2.flip(frame, 1)

        if cv2.waitKey(1) == 32:
            is_there_snack = not is_there_snack
            attempt += 1

        if cv2.waitKey(1) == 113:
            break

        if ret:
            frame_no += 1
            if is_there_snack:
                save_name = f'./snack_data/snack{snack_no}/'+'img_'+str(is_there_snack)+'_'+str(attempt)+'_'+str(frame_no)+'.jpg'
                cv2.imwrite(save_name, frame)
                frame = cv2.rectangle(frame, (0, 0), (50, 50), (0, 255, 0), 2)
                cv2.imshow('img', frame)
            else:
                save_name = './snack_data/snack0/'+'img_'+str(is_there_snack)+'_'+str(attempt)+'_'+str(frame_no)+'.jpg'
                cv2.imwrite(save_name, frame)
                frame = cv2.rectangle(frame, (0, 0), (50, 50), (0, 0, 255), 2)
                cv2.imshow('img', frame)
        else:
            print('no frame')
else:
    print("can't open camera")


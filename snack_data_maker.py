import cv2

is_there_snack = True
attempt = 1

cap = cv2.VideoCapture(0)
if cap.isOpened():
    frame_no = 0
    while True:
        ret, frame = cap.read()
        if ret:
            if is_there_snack:
                frame_no += 1
                cv2.imshow('img', frame)
                save_name = './snack_data/snack_yes/'+'img_'+str(is_there_snack)+'_'+str(attempt)+'_'+str(frame_no)+'.jpg'
                cv2.imwrite(save_name, frame)
            else:
                frame_no += 1
                cv2.imshow('img', frame)
                save_name = './snack_data/snack_no/'+'img_'+str(is_there_snack)+'_'+str(attempt)+'_'+str(frame_no)+'.jpg'
                cv2.imwrite(save_name, frame)
        else:
            print('no frame')
else:
    print("can't open camera")


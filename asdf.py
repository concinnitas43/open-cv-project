"""
함수들을 모은 파일이다.
"""

import dearpygui.dearpygui as dpg
import cv2
from image_id import unselected_config, selected_config
from screeninfo import get_monitors

from cnn.classifier import *
from audio.tts import *

"""
Monitor의 해상도를 얻어오는 과정. screeninfo 라이브러리의 get_monitors를 사용하였다.
"""
m = get_monitors()[0]
WIDTH, HEIGHT = m.width, m.height-89

def Video():
    """_summary_
    Vidoe 함수는 버튼 s(Setting)을 누르면 videocapture Window(창)이 꺼지고  Setting_Window(창)이 뜬다.
    버튼 q(Quit)을 누르면 종료된다.

    Args:
        None
    Raises:
        None
    Returns:
        None
    """
    dpg.minimize_viewport() 
    # 초기 설정시 dpg.window(show=False)는 가능하지만Viewport는 show False기능이 없다. \
    # 때문에 viewport를 꺼지게 한다.
    cap = cv2.VideoCapture(0) # 비디오 캡쳐하기
    while True:
        ret, frame = cap.read() # 비디오캡쳐 정보 읽기
        if not ret: # 못읽으면 예외처리
            break
        cv2.imshow('Video Capture', frame) # 캡쳐된거 보여주기

        key = cv2.waitKey(1) # 키 입력을 1ms 만큼 기다림 
        if key == ord('s'): # 만약 key가 s 면 loop 탈출
            key = 's'
            break
        if key == ord('q'): # 만약 key가 q 면 꺼짐 dpg의 context 공간(storge)를 비워줌(=초기화)
            dpg.destroy_context()
            break
        if key == ord(' '):
            snack_type = classify_image(frame)
            print(f"SNACK TYPE : {snack_type}")
            tts_speak(snack_type)

    cap.release() # vidoe release
    cv2.destroyAllWindows() # windows reset

    if key == 's': # key가 s일때 window 전환 기능 구현
        dpg.maximize_viewport() # view port가 화면 중앙정렬이 안되기에 height, width 설정만으로는 보기에 좋지 않음
        dpg.configure_item("setting_window", show=True) # Main widow show True
        dpg.configure_item("detailed_settings_window", show=False) # Specific window show False

def Resume_click(sender, app_data, user_data):
    """_summary_
    Resuem 버튼을 누르면 Main Window(settings_window)가 꺼지고 video window가 켜지게 하는 함수

    Args:
        sender: deatpygui에는 tag 시스템이 있다. 객체 고유 id와 유사하고 sender은 callback함수가 종속된 객체의 id이다.
            sender에는 그 객체의 정보가 key:value 형식으로 저장돼있다.
        app_data: 앱의 데이터 안 쓰인다.
        user_data: 유저가 동작한 데이터 안쓰인다.
    Raises:
        None
    Returns:
        None
    """
    dpg.configure_item("setting_window", show=False) # Main widow show False
    dpg.configure_item("detailed_settings_window", show=False) # Specific window show False
    Video() # Video 함수 실행
  
def Settings_click(sender, app_data, user_data):
    """_summary_
    Settings 버튼을 누르면 main setting window 에서 specific setting window로 넘어간다. 

    Args:
        sender: deatpygui에는 tag 시스템이 있다. 객체 고유 id와 유사하고 sender은 callback함수가 종속된 객체의 id이다.
            sender에는 그 객체의 정보가 key:value 형식으로 저장돼있다.
        app_data: 앱 데이터 안 쓰인다.
        user_data: 유저 입력 데이터 안쓰인다.
    Raises:
        None
    Returns:
        None
    """
    dpg.configure_item("setting_window", show=False) # Main widow show False
    dpg.configure_item("detailed_settings_window", show=True) # Specific window show True
    
def Volumn_slider(sender, app_data, user_data):
    """_summary_
    Sensitivity 아래 slider을 옮겨주면 Sensitivity 객체(dearpugui로 지정해준 변수공간의) 값을 app_data로 설정해준다
    
    Args:
        sender: deatpygui에는 tag 시스템이 있다. 객체 고유 id와 유사하고 sender은 callback함수가 종속된 객체의 id이다.
            sender에는 그 객체의 정보가 key:value 형식으로 저장돼있다.
        app_data: 앱의 데이터 안 쓰인다.
        user_data: 유저 입력 데이터 안쓰인다.
    Raises:
        None
    Returns:
        None
    """
    dpg.set_value("Volumn", app_data) # tag가 Sensitivity인 변수의 값을 app_data로 조정

def Exit_click(sender, app_data, user_data):
    """_summary_
    Exit 버튼은 Specific setting window에 있고 누르면 main setting window로 이동한다.

    Args:
        sender: deatpygui에는 tag 시스템이 있다. 객체 고유 id와 유사하고 sender은 callback함수가 종속된 객체의 id이다.
            sender에는 그 객체의 정보가 key:value 형식으로 저장돼있다.
        app_data: 앱의 데이터 안 쓰인다.
        user_data: 유저 입력 데이터 안쓰인다.
    Raises:
        None
    Returns:
        None
    """
    dpg.configure_item("setting_window", show=True) # Main widow show True
    dpg.configure_item("detailed_settings_window", show=False) # Specific window show False
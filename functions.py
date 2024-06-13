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
            pn = dpg.get_value('ProductName')
            pp = dpg.get_value('ProductPrice')
            ev = dpg.get_value('EventInfo')
            shi = dpg.get_value('ShortInfo')
            spi = dpg.get_value('SpecificInfo')
            vol = dpg.get_value('Volume')
            info_state = {'ProductName':pn, 'ProductPrice':pp, 'EventInfo':ev, 'ShortInfo':shi, 'SpecificInfo': spi}
            tts_speak(snack_type, vol, info_state)

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
    
def Volume_slider(sender, app_data, user_data):
    """_summary_
    Volume 아래 slider을 옮겨주면 Volume 객체(dearpugui로 지정해준 변수공간의) 값을 app_data로 설정해준다
    
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
    dpg.set_value("Volume", app_data) # tag가 Volume인 변수의 값을 app_data로 조정

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

def ProductName_click(sender, app_data, user_data):
    """_summary_
    버튼을 누르면 dpg context 공간의 변수 중 tag가 ProductName인 변수의 값을(Bool형) 전환한다.

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
    current_texture = dpg.get_item_configuration(sender)["texture_tag"]
    """
    윗 줄 코드 설명 get_item_configuration(sender)해서 sender의 정보 불러와서 key가 저거인걸 저장
    productname button은 dpg.add_image_button(texuture_tag=imgae)를 통해 이미지를 지정해준다. 
    image는 image_id.py에 있으며 selected, unselected가 있다. 

    (첨언, 이 설명은 image_id.py에도 있다.) main.py를 보면 이미지를 저장해주는 함수가 있음에도 별도로 image_id.py를 만들었다.
    그 이유는 sender의 texture_tag를 print해보면 main의 경우 str: selcted or unselcted인데 
    fuctions에서는 그 값이 int와 불규칙적 숫자로 저장된다.
    아마 dearpygui라이브러리에서 int id로 tag를 관리하는 것 같은데, 그것은 서칭해도 못찾았다.
    그래서 id(int)를 찾아주는 과정이 필요해 별도의 iamge_id.py를 만든것이다.
    또 그 숫자가 내 컴퓨터 환경에 종속되는지조차 알 수 없어, 새로운 dpg.create_context()을 통해 객채를 만들어주고
    그것의 id를 저장해주었다
    """ 
    if current_texture == unselected_config: # 만일 unselected라면 
        new_texture = selected_config       # selcted로 new로
        dpg.set_value("ProductName", True)  # set_value로 ProductName의 변수값을 True로 전환(info_state의 변수)
    else:
        new_texture = unselected_config     # unselcted로 전환
        dpg.set_value("ProductName", False) # set_value로 info_state 변수 값 전환
    dpg.configure_item(sender, texture_tag=new_texture) # image를 새로 할당
"""
아래 버튼들은 모두 ProductName_click 함수와 기능이 같다. 코드가 다 똑같아서 별도의 설명은 안적겠다.
클릭될 경우 image를 전환해주고 해당 변수(bool 형)값을 전환해준다.
"""
def ProductPrice_click(sender, app_data, user_data):
    current_texture = dpg.get_item_configuration(sender)["texture_tag"]
    if current_texture == unselected_config:
        new_texture = selected_config
        dpg.set_value("ProductPrice", True)
    else:
        new_texture = unselected_config
        dpg.set_value("ProductPrice", False)
    dpg.configure_item(sender, texture_tag=new_texture)
 
def EventInfo_click(sender, app_data, user_data):
    current_texture = dpg.get_item_configuration(sender)["texture_tag"]
    if current_texture == unselected_config:
        new_texture = selected_config
        dpg.set_value("EventInfo", True)
    else:
        new_texture = unselected_config
        dpg.set_value("EventInfo", False)
    dpg.configure_item(sender, texture_tag=new_texture)

def ShortInfo_click(sender, app_data, user_data):
    current_texture = dpg.get_item_configuration(sender)["texture_tag"]
    if current_texture == unselected_config:
        new_texture = selected_config
        dpg.set_value("ShortInfo", True)
    else:
        new_texture = unselected_config
        dpg.set_value("ShortInfo", False)
    dpg.configure_item(sender, texture_tag=new_texture)

def SpecificInfo_click(sender, app_data, user_data):
    current_texture = dpg.get_item_configuration(sender)["texture_tag"]
    if current_texture == unselected_config:
        new_texture = selected_config
        dpg.set_value("SpecificInfo", True)
    else:
        new_texture = unselected_config
        dpg.set_value("SpecificInfo", False)
    dpg.configure_item(sender, texture_tag=new_texture)
"""
main.py를 보면 이미지를 저장해주는 함수가 있음에도 별도로 image_id.py를 만들었다.
그 이유는 sender의 texture_tag를 print해보면 main의 경우 str: selcted or unselcted인데 
fuctions에서는 그 값이 int와 불규칙적 숫자로 저장된다.
아마 dearpygui라이브러리에서 int id로 tag를 관리하는 것 같은데, 그것은 서칭해도 못찾았다.
그래서 id(int)를 찾아주는 과정이 필요해 별도의 iamge_id.py를 만든것이다.
또 그 숫자가 내 컴퓨터 환경에 종속되는지조차 알 수 없어, 새로운 dpg.create_context()을 통해 객채를 만들어주고
그것의 id를 저장해주었다
"""


import dearpygui.dearpygui as dpg
dpg.create_context() # context 공간 생성

#초기값 설정
unselected_config=0
selected_config=0

"""
텍스쳐 공간 맏들기

이미지 불러오고 static(변하지않는 texture(보통 이미지 씀)) value 를 할당
"""
with dpg.texture_registry():
    width, height, channels, data = dpg.load_image("./resources/circle_button_unselected.png") # 이미지 로드
    unselected = dpg.add_static_texture(width=width, height=height, default_value=data, tag="unselected") # 이미지 객체로 할당

with dpg.texture_registry():
    width, height, channels, data = dpg.load_image("./resources/circle_button_selected.png")# 이미지 로드
    selected = dpg.add_static_texture(width=width, height=height, default_value=data, tag="selected") # 이미지 객체로 할당
"""
winodw 생성(딱히 파라미터값 할당 안해줘서 안보임)
imagee_button add한 다음에 get_item_configuration 해서 int값 얻는다
"""
with dpg.window():
    dpg.add_image_button(texture_tag=unselected, show=False, tag='UNSELECTED') # 버튼에 이미지 할당
    dpg.add_image_button(texture_tag=selected, show=False, tag='SELECTED')  # 버튼에 이미지 할당

    unselected_config = dpg.get_item_configuration('UNSELECTED')['texture_tag'] # 버튼에서 이미지 ID(추정) int값 얻기
    selected_config = dpg.get_item_configuration('SELECTED')['texture_tag'] # 버튼에서 이미지 ID(추정) int값 얻기
dpg.destroy_context() # 초기화
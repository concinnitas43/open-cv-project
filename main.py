from informations import *
#from buttons_info import home_buttons, settings_buttons, names
"""
메인 파일이다.
"""
dpg.create_context() # dpg의 context들의 space를 create
"""
텍스텨 저장소
selcted / unselcted 이미지를 저장한다
"""
with dpg.texture_registry(): # 저장소에서
    width, height, channels, data = dpg.load_image("./resources/circle_button_unselected.png") #이미지 불러오고
    unselected = dpg.add_static_texture(width=width, height=height, default_value=data, tag="unselected") #변수에 저장

with dpg.texture_registry(): #아래와 동일하다
    width, height, channels, data = dpg.load_image("./resources/circle_button_selected.png")
    selected = dpg.add_static_texture(width=width, height=height, default_value=data, tag="selected")
"""
폰트 저장소
폰트를 불러오고 사이즈별 폰트를 저장소에 저장해준다
***dpg상에서 font의 size를 조절하는 함수가 없다. font자체에 사이즈가 포함되어 있는 포멧이다.***
"""
def font_size(n): # 폰트 저장해주는 함수
    return dpg.add_font("./resources/Roboto-Light.ttf", n) # 폰트 추가하기

with dpg.font_registry(): # 폰트 저장소에서 사이즈별 저장 (5개)
    font10=font_size(10)
    font20=font_size(20)
    font30=font_size(30)
    font40=font_size(40)
    font50=font_size(50)
"""
변수 저장소
tts.py에서 쓰일 변수들로
이것에 따라 volume조절이 가능하고, TTS로 들려줄 정보의 종류를 고를 수 있다.
"""
with dpg.value_registry():
    dpg.add_bool_value(default_value=False, tag='ProductName') # 테그(ID)가 ProductName인 bool타입 value 저장
    dpg.add_bool_value(default_value=False, tag='ProductPrice') 
    dpg.add_bool_value(default_value=False, tag='EventInfo')
    dpg.add_bool_value(default_value=False, tag='ShortInfo')
    dpg.add_bool_value(default_value=False, tag='SpecificInfo')
    dpg.add_int_value(default_value=30, tag='Volume') # int타입 value 저장

"""
Button 객체 Class이다.
라벨, 콜벡함수, 위치, width, height, tag 를 init으로 갖는다

create 함수가 있는데 circle(selcted, unselcted)라면 
    add_image_button으로 이미지 형식 저장 (dpg에는 버튼이 직사각형뿐이다)
    아니라면 add_button으로 저장한다.
"""
class MyButton:
    def __init__(self, label, click_callback, pos = None, width= None, height=None):
        self.label = label
        self.click_callback = click_callback
        self.button_id = None
        self.pos = pos
        self.width = width
        self.height = height
        self.tag=label

    def create(self, circle=False, image=None):
        if circle:
            self.tag = f'{self.label}_Button'
            self.button_id = dpg.add_image_button(texture_tag=image, label=self.label, callback=self.click_callback,\
                                                pos = self.pos, width=self.width, height=self.height, tag=self.tag)
        else:
            self.button_id = dpg.add_button(label=self.label, callback=self.click_callback,\
                                                pos = self.pos, width=self.width, height=self.height, tag=self.tag)
"""
button을 MyButton클래스로 만들어주는 과정.
"""
for buttonset in [home_buttons, settings_buttons]:
    for button_name in buttonset.keys():
        buttonset[button_name] = MyButton(label=f"{button_name}", click_callback=buttons__fucs[button_name], pos=buttonset[button_name][0],\
                                            width = buttonset[button_name][1][0], height = buttonset[button_name][1][1])
"""
window를 생성하고 거기서 버튼을 넣어주고 폰트를 조절해준다
"""
with dpg.window(label="Setting Window", show=False, width=WIDTH, height=HEIGHT, pos=(0, 0), no_close=True, tag='setting_window'): # window 생성
    dpg.bind_font(font20) # 전체 폰트 할당
    for button in home_buttons.values(): # 버튼 만들기
        button.create()
        dpg.bind_item_font(button.tag, font30) # 각 버튼의 폰트 할당
with dpg.window(label="Detailed Settings Window", show=False, width=WIDTH, height=HEIGHT, pos=(0, 0), no_close=True,tag='detailed_settings_window'): # window 생성
    dpg.bind_font(font20) # 전체 폰트 할당
    for button in settings_buttons.values(): # 버튼 만들기
            if button.label in info_buttons:
                if button.label == 'ProductName':
                    button.create(circle=True, image=selected) # productname은 초기갑이 selcted
                else:
                    button.create(circle=True, image=unselected) # image 초기에는 uselcted
            else:
                button.create()
                dpg.bind_item_font(button.tag, font20) # 버튼 폰트 설정
    s1 = dpg.add_text("Volume", pos=(9/30*WIDTH-125,1/2*HEIGHT-150)) # 텍스트 Volume 넣기
    dpg.bind_item_font(s1, font40) # Volum 폰트 설정
    s2 = dpg.add_text("InforState", pos=(11/15*WIDTH-125,1/2*HEIGHT-150)) # inforstate 넣기 텍스트
    dpg.bind_item_font(s2, font40) # inforstate 텍스트 폰트 설정
    for b, position in info_pos.items():
        bt = dpg.add_text(b, pos=(position[0][0]+30, position[0][1]-5)) # inforstate 그룹의 애들 텍스트 설정 (productname, price 등)
    # 슬라이드 만들기(volume 거)
    dpg.add_slider_int(pos=(1/5*WIDTH-60,1/2*HEIGHT),\
                       width=400, height=50,\
                    track_offset=0.3, min_value=0, default_value=30, max_value=100, callback=Volume_slider)

# viewport 만들어주기 (window는 화면 속 객체고 viewport가 전체이미지임)
dpg.create_viewport(title='What is Your Name', width=WIDTH, height=HEIGHT+89)
# 초기설정
dpg.setup_dearpygui()
#비디오 실행
Video()
#이후에 뷰포트 보여주기
dpg.show_viewport()
#dpg가 동적이게(start해주기)
dpg.start_dearpygui()
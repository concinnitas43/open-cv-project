from informations import *
#from buttons_info import home_buttons, settings_buttons, names
dpg.create_context()

with dpg.texture_registry():
    width, height, channels, data = dpg.load_image("./resources/circle_button_unselected.png")
    unselected = dpg.add_static_texture(width=width, height=height, default_value=data, tag="unselected")

with dpg.texture_registry():
    width, height, channels, data = dpg.load_image("./resources/circle_button_selected.png")
    selected = dpg.add_static_texture(width=width, height=height, default_value=data, tag="selected")

def font_size(n: int):
    return dpg.add_font("./resources/Roboto-Light.ttf", n)

with dpg.font_registry():
    font10=font_size(10)
    font20=font_size(20)
    font30=font_size(30)
    font40=font_size(40)
    font50=font_size(50)

with dpg.value_registry():
    dpg.add_bool_value(default_value=False, tag='ProductName')
    dpg.add_bool_value(default_value=False, tag='ProductPrice')
    dpg.add_bool_value(default_value=False, tag='EventInfo')
    dpg.add_bool_value(default_value=False, tag='ShortInfo')
    dpg.add_bool_value(default_value=False, tag='SpecificInfo')
    dpg.add_int_value(default_value=30, tag='Volumn')


class MyButton:
    def __init__(self, label, click_callback, pos = None, width= None, height=None, unslec_num=None, selc_num=None):
        self.label = label
        self.click_callback = click_callback
        self.button_id = None
        self.pos = pos
        self.width = width
        self.height = height
        self.tag=label
        self.unselc=unslec_num
        self.selc=selc_num

    def create(self, circle=False, image=None):
        if circle:
            self.tag = f'{self.label}_Button'
            self.button_id = dpg.add_image_button(texture_tag=image, label=self.label, callback=self.click_callback,\
                                                pos = self.pos, width=self.width, height=self.height, tag=self.tag)
        else:
            self.button_id = dpg.add_button(label=self.label, callback=self.click_callback,\
                                                pos = self.pos, width=self.width, height=self.height, tag=self.tag)

for buttonset in [home_buttons, settings_buttons]:
    for button_name in buttonset.keys():
        buttonset[button_name] = MyButton(label=f"{button_name}", click_callback=buttons__fucs[button_name], pos=buttonset[button_name][0],\
                                            width = buttonset[button_name][1][0], height = buttonset[button_name][1][1])
with dpg.window(label="Setting Window", show=False, width=WIDTH, height=HEIGHT, pos=(0, 0), no_close=True, tag='setting_window'):
    dpg.bind_font(font20)
    for button in home_buttons.values():
        button.create()
        dpg.bind_item_font(button.tag, font30)
with dpg.window(label="Detailed Settings Window", show=False, width=WIDTH, height=HEIGHT, pos=(0, 0), no_close=True,tag='detailed_settings_window'):
    dpg.bind_font(font20)
    for button in settings_buttons.values():
            if button.label in info_buttons:
                button.create(circle=True, image=unselected)#, unselc_num=unselected_config, selc_num=selected_config)
            else:
                button.create()
                dpg.bind_item_font(button.tag, font20)
    s1 = dpg.add_text("Volumn", pos=(9/30*WIDTH-125,1/2*HEIGHT-150))
    dpg.bind_item_font(s1, font40)
    s2 = dpg.add_text("InforState", pos=(11/15*WIDTH-125,1/2*HEIGHT-150))
    dpg.bind_item_font(s2, font40)
    for b, position in info_pos.items():
        bt = dpg.add_text(b, pos=(position[0][0]+30, position[0][1]-5))
    dpg.add_slider_int(pos=(1/5*WIDTH-60,1/2*HEIGHT),\
                       width=400, height=50,\
                    track_offset=0.3, min_value=0, default_value=30, max_value=100, callback=Volumn_slider)


dpg.create_viewport(title='What is Your Name', width=WIDTH, height=HEIGHT+89)
dpg.setup_dearpygui()

Video()
dpg.show_viewport()
dpg.start_dearpygui()
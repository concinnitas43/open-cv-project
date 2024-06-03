import dearpygui.dearpygui as dpg
from functions import *
#from buttons_info import home_buttons, settings_buttons, names
dpg.create_context()



WIDTH = 1200
HEIGHT = 600
names = ['Resume', 'Settings' ,'Sensitivity', 'Exit', 'ProductName', 'ProductPrice', 'EventInfo', 'ShortInfo', 'SpecificInfo']

home_buttons={'Settings':[(11/16*WIDTH-125,1/2*HEIGHT-100), (250, 200)], 'Resume':[(5/16*WIDTH-125,1/2*HEIGHT-100), (250, 200)]}
settings_buttons={'Exit': [(WIDTH-60, 30), (50, 30)],\
                  'ProductName':[(11/16*WIDTH-125,1/2*HEIGHT-90), (10, 10)],\
                    'ProductPrice':[(11/16*WIDTH-125,1/2*HEIGHT-45), (10, 10)], 'EventInfo':[(11/16*WIDTH-125,1/2*HEIGHT), (10, 10)],\
                    'ShortInfo':[(11/16*WIDTH-125,1/2*HEIGHT+45), (10, 10)], 'SpecificInfo':[(11/16*WIDTH-125,1/2*HEIGHT+90), (10, 10)]}
info_pos = {'ProductName':[(11/16*WIDTH-125,1/2*HEIGHT-90), (10, 10)],\
                    'ProductPrice':[(11/16*WIDTH-125,1/2*HEIGHT-45), (10, 10)], 'EventInfo':[(11/16*WIDTH-125,1/2*HEIGHT), (10, 10)],\
                    'ShortInfo':[(11/16*WIDTH-125,1/2*HEIGHT+45), (10, 10)], 'SpecificInfo':[(11/16*WIDTH-125,1/2*HEIGHT+90), (10, 10)]}
info_buttons = ['ProductName', 'ProductPrice', 'EventInfo', 'ShortInfo', 'SpecificInfo']
# 'Sensitivity':Sensitivity_slider  'Sensitivity':[(11/16*WIDTH-125,1/2*HEIGHT-100), (1,1)],
buttons__fucs = {'Resume':Resume_click, 'Settings':Settings_click,\
                'Exit':Exit_click, 'ProductName':ProductName_click, 'ProductPrice':ProductPrice_click,\
            'EventInfo':EventInfo_click, 'ShortInfo':ShortInfo_click, 'SpecificInfo':SpecificInfo_click}
with dpg.value_registry():
    dpg.add_bool_value(default_value=False, tag='ProductName')
    dpg.add_bool_value(default_value=False, tag='ProductPrice')
    dpg.add_bool_value(default_value=False, tag='EventInfo')
    dpg.add_bool_value(default_value=False, tag='ShortInfo')
    dpg.add_bool_value(default_value=False, tag='SpecificInfo')
    dpg.add_int_value(default_value=3, tag='Sensitivity')
with dpg.texture_registry():
    width, height, channels, data = dpg.load_image("cricle_button_unselected.png")
    unselected = dpg.add_static_texture(width=width, height=height, default_value=data, tag="unselected")
with dpg.texture_registry():
    width, height, channels, data = dpg.load_image("cricle_button_selected.png")
    selected = dpg.add_static_texture(width=width, height=height, default_value=data, tag="selected")
def font_size(n: int):
        return dpg.add_font("./Roboto-Light.ttf", n)
with dpg.font_registry():
    font10=font_size(10)
    font20=font_size(20)
    font30=font_size(30)
    font40=font_size(40)
    font50=font_size(50)

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
            self.tag = f'{self.label}_{image}'
            self.button_id = dpg.add_image_button(texture_tag=image, label=self.label, callback=self.click_callback,\
                                                pos = self.pos, width=self.width, height=self.height, tag=self.tag)
        else:
            self.button_id = dpg.add_button(label=self.label, callback=self.click_callback,\
                                                pos = self.pos, width=self.width, height=self.height, tag=self.tag)

for buttonset in [home_buttons, settings_buttons]:
    for button_name in buttonset.keys():
        buttonset[button_name] = MyButton(label=f"{button_name}", click_callback=buttons__fucs[button_name], pos=buttonset[button_name][0],\
                                            width = buttonset[button_name][1][0], height = buttonset[button_name][1][1])
with dpg.window(label="Setting Window", width=WIDTH, height=HEIGHT, pos=(0, 0), no_close=True, tag='setting_window'):
    dpg.bind_font(font20)
    for button in home_buttons.values():
        button.create()
        dpg.bind_item_font(button.tag, font30)
with dpg.window(label="Detailed Settings Window", width=WIDTH, height=HEIGHT, pos=(0, 0), no_close=True,tag='detailed_settings_window'):
    dpg.bind_font(font20)
    for button in settings_buttons.values():
            if button.label in info_buttons:
                button.create(circle=True, image=unselected)#, unselc_num=unselected_config, selc_num=selected_config)
            else:
                button.create()
                dpg.bind_item_font(button.tag, font20)
    s1 = dpg.add_text("Sensitivity", pos=(4/15*WIDTH-125,1/2*HEIGHT-150))
    dpg.bind_item_font(s1, font40)
    s2 = dpg.add_text("InforState", pos=(11/15*WIDTH-125,1/2*HEIGHT-150))
    dpg.bind_item_font(s2, font40)
    for b, position in info_pos.items():
        bt = dpg.add_text(b, pos=(position[0][0]+30, position[0][1]-5))
    dpg.add_slider_int(pos=(1/5*WIDTH-125,1/2*HEIGHT),\
                       width=400, height=50,\
                    track_offset=0.3, min_value=3, max_value=10, callback=Sensitivity_slider)


# Setup viewport
dpg.create_viewport(title='What is Your Name', width=WIDTH+50, height=HEIGHT+80)
dpg.setup_dearpygui()
dpg.show_viewport()
# Initially show the home window and hide the settings window
dpg.configure_item("setting_window", show=True)
dpg.configure_item("detailed_settings_window", show=False)

# Start Dear PyGui event loop
dpg.start_dearpygui()

# Destroy context when done
dpg.destroy_context()

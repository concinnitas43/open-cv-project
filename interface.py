import dearpygui.dearpygui as dpg
from functions import *
#from buttons_info import home_buttons, settings_buttons, names
dpg.create_context()

WIDTH = 1200
HEIGHT = 600
names = ['Resume', 'Settings' ,'Sensitivity', 'Exit', 'ProductName', 'ProductPrice', 'EventInfo', 'ShortInfo', 'SpecificInfo']

home_buttons={'Settings':[(11/16*WIDTH-125,1/2*HEIGHT-100), (250, 200)], 'Resume':[(5/16*WIDTH-125,1/2*HEIGHT-100), (250, 200)]}
settings_buttons={'Exit': [(WIDTH-50, 20), (50, 30)],\
                  'ProductName':[(11/16*WIDTH-125,1/2*HEIGHT-60), (10, 10)],\
                    'ProductPrice':[(11/16*WIDTH-125,1/2*HEIGHT-30), (10, 10)], 'EventInfo':[(11/16*WIDTH-125,1/2*HEIGHT), (10, 10)],\
                    'ShortInfo':[(11/16*WIDTH-125,1/2*HEIGHT+30), (10, 10)], 'SpecificInfo':[(11/16*WIDTH-125,1/2*HEIGHT+60), (10, 10)]}
info_buttons = ['ProductName', 'ProductPrice', 'EventInfo', 'ShortInfo', 'SpecificInfo']
# 'Sensitivity':Sensitivity_slider  'Sensitivity':[(11/16*WIDTH-125,1/2*HEIGHT-100), (1,1)],
buttons__fucs = {'Resume':Resume_click, 'Settings':Settings_click,\
                'Exit':Exit_click, 'ProductName':ProductName_click, 'ProductPrice':ProductPrice_click,\
            'EventInfo':EventInfo_click, 'ShortInfo':ShortInfo_click, 'SpecificInfo':SpecificInfo_click}
with dpg.texture_registry():
    width, height, channels, data = dpg.load_image("cricle_button_unselected.png")
    unselected = dpg.add_static_texture(width=width, height=height, default_value=data, tag="unselected")
with dpg.texture_registry():
    width, height, channels, data = dpg.load_image("cricle_button_selected.png")
    selected = dpg.add_static_texture(width=width, height=height, default_value=data, tag="selected")


class MyButton:
    def __init__(self, label, click_callback, pos = None, width= None, height=None, tag=None):
        self.label = label
        self.click_callback = click_callback
        self.button_id = None
        self.pos = pos
        self.width = width
        self.height = height
        self.tag=label

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
                                            width = buttonset[button_name][1][0], height = buttonset[button_name][1][1], tag='button_name')
# Create a window and add widgets
with dpg.window(label="Setting Window", width=WIDTH, height=HEIGHT, pos=(0, 0), no_close=True, tag='setting_window'):
    for button in home_buttons.values():
        button.create()

with dpg.window(label="Detailed Settings Window", width=WIDTH, height=HEIGHT, pos=(0, 0), no_close=True,tag='detailed_settings_window'):
    for button in settings_buttons.values():
            if button.label in info_buttons:
                button.create(circle=True, image=unselected)
            else:
                button.create()
    dpg.add_slider_int(label="Sensitivity",pos=(5/16*WIDTH-125,1/2*HEIGHT-100),\
                       width=400, height=100,\
                    track_offset=0.3, min_value=3, max_value=10, callback=Sensitivity_slider)
    dpg.add_text(label="", tag="Sensitivity", pos=(0, 0))

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

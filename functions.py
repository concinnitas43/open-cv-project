import dearpygui.dearpygui as dpg
import cv2
from image_id import unselected_config, selected_config
from screeninfo import get_monitors

m = get_monitors()[0]
WIDTH, HEIGHT = m.width, m.height-89

def Video():
    dpg.minimize_viewport()
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Video Capture', frame)

        key = cv2.waitKey(1) 
        if key == ord('s'):
            key = 's'
            break
        if key == ord('q'):
            dpg.destroy_context()
            break
    cap.release()
    cv2.destroyAllWindows()

    if key == 's':
        dpg.maximize_viewport()
        dpg.configure_item("setting_window", show=True)
        dpg.configure_item("detailed_settings_window", show=False)

def Resume_click(sender, app_data, user_data):
    dpg.configure_item("setting_window", show=False)
    dpg.configure_item("detailed_settings_window", show=False)
    Video()
  
def Settings_click(sender, app_data, user_data):
    dpg.configure_item("setting_window", show=False)
    dpg.configure_item("detailed_settings_window", show=True)
    
def Sensitivity_slider(sender, app_data, user_data):
    #Slider value: {app_data}
    dpg.set_value("Sensitivity", app_data)
    #print(dpg.get_value("Sensitivity"))

def Exit_click(sender, app_data, user_data):
    dpg.configure_item("setting_window", show=True)
    dpg.configure_item("detailed_settings_window", show=False)

def ProductName_click(sender, app_data, user_data):
    current_texture = dpg.get_item_configuration(sender)["texture_tag"]
    if current_texture == unselected_config:
        new_texture = selected_config
        dpg.set_value("ProductName", True)
        #print(dpg.get_value("ProductName"))
    else:
        new_texture = unselected_config
        dpg.set_value("ProductName", False)
    dpg.configure_item(sender, texture_tag=new_texture)

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
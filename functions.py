import dearpygui.dearpygui as dpg


def Resume_click(sender, app_data, user_data):
    dpg.set_value("label", "Button Clicked!")
    
def Settings_click(sender, app_data, user_data):
    dpg.configure_item("setting_window", show=False)
    dpg.configure_item("detailed_settings_window", show=True)
    
def Sensitivity_slider(sender, app_data, user_data):
    #Slider value: {app_data}
    dpg.set_value("Sensitivity", f"Sensitivity value: {app_data}")

def Exit_click(sender, app_data, user_data):
    dpg.configure_item("setting_window", show=True)
    dpg.configure_item("detailed_settings_window", show=False)

def ProductName_click(sender, app_data, user_data):
    current_texture = dpg.get_item_configuration(sender)["texture_tag"]
    new_texture = 24 if current_texture == 22 else 22
    dpg.configure_item(sender, texture_tag=new_texture)

def ProductPrice_click(sender, app_data, user_data):
    current_texture = dpg.get_item_configuration(sender)["texture_tag"]
    new_texture = 24 if current_texture == 22 else 22
    dpg.configure_item(sender, texture_tag=new_texture)
 
def EventInfo_click(sender, app_data, user_data):
    current_texture = dpg.get_item_configuration(sender)["texture_tag"]
    new_texture = 24 if current_texture == 22 else 22
    dpg.configure_item(sender, texture_tag=new_texture)

def ShortInfo_click(sender, app_data, user_data):
    current_texture = dpg.get_item_configuration(sender)["texture_tag"]
    new_texture = 24 if current_texture == 22 else 22
    dpg.configure_item(sender, texture_tag=new_texture)

def SpecificInfo_click(sender, app_data, user_data):
    current_texture = dpg.get_item_configuration(sender)["texture_tag"]
    new_texture = 24 if current_texture == 22 else 22
    dpg.configure_item(sender, texture_tag=new_texture)


import dearpygui.dearpygui as dpg
dpg.create_context()

unselected_config=0
selected_config=0
with dpg.texture_registry():
    width, height, channels, data = dpg.load_image("./resources/circle_button_unselected.png")
    unselected = dpg.add_static_texture(width=width, height=height, default_value=data, tag="unselected")

with dpg.texture_registry():
    width, height, channels, data = dpg.load_image("./resources/circle_button_selected.png")
    selected = dpg.add_static_texture(width=width, height=height, default_value=data, tag="selected")

with dpg.window():
    # Add buttons to check the assigned integer values
    dpg.add_image_button(texture_tag=unselected, show=False, tag='UNSELECTED')
    
    dpg.add_image_button(texture_tag=selected, show=False, tag='SELECTED')

    # Retrieve the configuration to check the texture tags
    unselected_config = dpg.get_item_configuration('UNSELECTED')['texture_tag']
    selected_config = dpg.get_item_configuration('SELECTED')['texture_tag']
dpg.destroy_context()
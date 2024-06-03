import dearpygui.dearpygui as dpg

def slider_callback(sender, app_data, user_data):
    print(f"Sender: {sender}")
    print(f"Slider value: {app_data}")
    print(f"User data: {user_data}")
    dpg.set_value("label", f"Slider value: {app_data}")

dpg.create_context()

with dpg.window(label="Example Window"):
    dpg.add_slider_float(label="Slider", min_value=3, max_value=10, default_value=3, format='%d',\
                        callback=slider_callback, user_data="Extra data")
    dpg.add_text(label="", tag="label")
    dpg.add_text(label="", tag="Sensitivity", pos=(0, 0))

dpg.create_viewport(title='Callback Example', width=600, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()

dpg.start_dearpygui()
dpg.destroy_context()

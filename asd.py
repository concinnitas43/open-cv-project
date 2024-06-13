from asdf import *

names = ['Resume', 'Settings' ,'Volum', 'Exit']
home_buttons={'Settings':[(11/16*WIDTH-125,1/2*HEIGHT-100), (250, 200)], 'Resume':[(5/16*WIDTH-125,1/2*HEIGHT-100), (250, 200)]}
settings_buttons={'Exit': [(WIDTH-60, 30), (50, 30)]}
buttons__fucs = {'Resume':Resume_click, 'Settings':Settings_click,\
                'Exit':Exit_click}


from functions import *

names = ['Resume', 'Settings' ,'Volumn', 'Exit', 'ProductName', 'ProductPrice', 'EventInfo', 'ShortInfo', 'SpecificInfo']
home_buttons={'Settings':[(11/16*WIDTH-125,1/2*HEIGHT-100), (250, 200)], 'Resume':[(5/16*WIDTH-125,1/2*HEIGHT-100), (250, 200)]}
settings_buttons={'Exit': [(WIDTH-60, 30), (50, 30)],\
                  'ProductName':[(11/16*WIDTH-125,1/2*HEIGHT-90), (10, 10)],\
                    'ProductPrice':[(11/16*WIDTH-125,1/2*HEIGHT-45), (10, 10)], 'EventInfo':[(11/16*WIDTH-125,1/2*HEIGHT), (10, 10)],\
                    'ShortInfo':[(11/16*WIDTH-125,1/2*HEIGHT+45), (10, 10)], 'SpecificInfo':[(11/16*WIDTH-125,1/2*HEIGHT+90), (10, 10)]}
info_pos = {'ProductName':[(11/16*WIDTH-125,1/2*HEIGHT-90), (10, 10)],\
                    'ProductPrice':[(11/16*WIDTH-125,1/2*HEIGHT-45), (10, 10)], 'EventInfo':[(11/16*WIDTH-125,1/2*HEIGHT), (10, 10)],\
                    'ShortInfo':[(11/16*WIDTH-125,1/2*HEIGHT+45), (10, 10)], 'SpecificInfo':[(11/16*WIDTH-125,1/2*HEIGHT+90), (10, 10)]}
info_buttons = ['ProductName', 'ProductPrice', 'EventInfo', 'ShortInfo', 'SpecificInfo']
buttons__fucs = {'Resume':Resume_click, 'Settings':Settings_click,\
                'Exit':Exit_click, 'ProductName':ProductName_click, 'ProductPrice':ProductPrice_click,\
            'EventInfo':EventInfo_click, 'ShortInfo':ShortInfo_click, 'SpecificInfo':SpecificInfo_click}


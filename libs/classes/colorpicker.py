from kivy.properties import StringProperty
from kivy.uix.dropdown import DropDown
from kivymd.uix.button import Button
from kivymd.uix.label import Label
from libs.classes.selection import Selection

from kivy.lang import Builder
import os
'''print("***---- in colorpicker.py: {} ".format(os.path.join(
                os.environ["PULSO_APP_ROOT"], "libs", "kv",
                "selection.kv")))'''
                
class ColorPicker(Selection):
    colors = {}
    
    # Layout for selecting items
    text_box = Label(text="...", color=(0,0,0,1))
    dropdown = DropDown()
    #color = None
    
    def __init__(self, **kwargs):
        print("Starting super")
        super(ColorPicker, self).__init__(**kwargs)
        print("finished super")
        '''self.app = MDApp.get_running_app()
        self.picker_btn = Button(text="Choose Color")
        self.picker_btn.bind(on_release=self.dropdown.open)
        self.add_widget(self.picker.picker_btn)
        self.add_widget(self.text_box)
        
        # Add colors to dropdown
        for color in colors:
            btn = Button(text=color)
            # When a color is selected the name is passed to dropdown object
            btn.bind(on_release = lambda btn : dropdown.select(btn.text) )
            self.dropdown.add_widget(btn)
            
        self.dropdown.bind(on_select= lambda instance, x: setattr(self, 'selection', x) )'''
from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivy.uix.dropdown import DropDown
from kivymd.uix.button import Button
from kivymd.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from libs.classes.selection import Selection

                
class Color_Picker(Selection):
    colors = {"Sky Blue":(0.529, 0.808, 0.922)}
    
        
    browse_btn = Button(text="Browse")
    #browse_btn.bind(on_release=lambda x : x.root.browse(x))
    # bind button to static FileBrowser' browse() function
    #browse_btn.bind(on_release=lambda x : FileBrowser.open(FileBrowser.instance))
    
    def __init__(self, **kwargs):
        super(Color_Picker, self).__init__(**kwargs)
        # Layout for selecting items
        self.dropdown = DropDown()
        self.app = MDApp.get_running_app()
        self.picker_btn.text="Choose Color"
        self.picker_btn.bind(on_release= self.dropdown.open)
        
        # Add colors to dropdown
        for color in self.colors:
            btn = Button(text=color, size_hint_y=None, height=40)
            # When a color is selected the name is passed to dropdown object
            btn.bind(on_release = lambda btn : self.dropdown.select(btn.text) )
            self.dropdown.add_widget(btn)
            
        self.dropdown.bind(on_select= lambda instance, x: setattr(self, 'selection', x) )
        
    def dismiss(self):
        self.dropdown.dismiss()
        
    def on_leave(self):
        self.dropdown.clear_widgets()
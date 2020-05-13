from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import Button
from kivymd.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.core.clipboard import Clipboard

class Settings_Setup(Screen):
    def __init__(self, **kwargs):
        #self.manager = manager
        super(Settings_Setup, self).__init__(**kwargs)
        
class Settings_cell(BoxLayout):
    topic = StringProperty()
    info = StringProperty()
    
    # Holds all the tags that go to editing operations
    changes = []

    def __init__(self, **kwargs):
        #self.manager = manager
        super(Settings_cell, self).__init__(**kwargs)
        
    def change(self):
        pass
        
    def buttons(self):
        if self.info in changes:
            self.change()
    
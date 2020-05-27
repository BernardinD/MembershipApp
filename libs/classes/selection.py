from kivymd.app import MDApp
from kivymd.uix.button import Button
from kivymd.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from kivy.lang import Builder
import os
'''Builder.load_file(os.path.join(
                os.environ["PULSO_APP_ROOT"], "libs", "kv",
                "selection.kv"))'''
class Selection(BoxLayout):
    
    '''picker_btn = Button(text="Browse")
    #browse_btn.bind(on_release=lambda x : x.root.browse(x))
    # bind button to static FileBrowser' browse() function
    picker_btn.bind(on_release=lambda x : FileBrowser.open(FileBrowser.instance))
    text_box = Label(text="...", color=(0,0,0,1))'''
    
    def __init__(self, **kwargs):
        
        print("Continuing super")
        super(Selection, self).__init__(**kwargs)
        print("returned Selection's super")
        '''self.app = MDApp.get_running_app()
        self.add_widget(self.picker_btn)
        self.add_widget(self.text_box)'''
from kivymd.app import MDApp
import os

from kivy.uix.filechooser import FileChooserListView
from kivymd.uix.button import Button
from kivymd.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from libs.classes.selection import Selection

class FileBrowser(Selection):
    '''
    This class is used to find files on the system.
    Currently it is only set to find image files
    '''
    text_box = Label(text="...", color=(0,0,0,1))
    
    def __init__(self, **kwargs):
        print("In FileBrowser")
        super(FileBrowser, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.Browser = Popup(size_hint=(0.75, 0.75))
        fc = FileChooserListView()
        fc.rootpath = os.environ["PULSO_APP_ROOT"]
        exit = Button(text='Cancel',
                        size_hint=(1, 0.1),
                        on_release=self.Browser.dismiss)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(fc)
        layout.add_widget(exit)
        self.Browser.add_widget(layout)
        
        fc.bind(selection= lambda instance, x: self.set_select(x))
        self.picker_btn.bind(on_release=lambda x : self.Browser.open(self.Browser))
    
    def set_select(self, x):
        '''
        Sets inherted 'selection' if a file selection was made 
        and it is an image
        '''
        img_types = ['jpg', 'jpeg', 'png']
        if len(x) > 0:
            check = x[0].lower()
            # Check if jpg or png
            if any(img_type in check for img_type in img_types):
                setattr(self, 'selection', x[0])
                self.Browser.dismiss()
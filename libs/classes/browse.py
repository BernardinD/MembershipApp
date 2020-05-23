from kivymd.app import MDApp
from kivy.uix.filechooser import FileChooserListView
from kivymd.uix.button import Button
from kivymd.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty



class FileBrowser(Popup):
    # Object openning browser
    root = None
    selection = StringProperty("")
    instance = None
    
    '''def __init__(self, **kwargs):
        super(FileBrowser, self).__init__(**kwargs)
        self.app = MDApp.get_running_app
        
    def browse(self, obj):
        # Open popup
        print("self = ", self)
        try:
            print(self.open(self))
        except Exception as e:
            print(e)
    # function callback for on_selection
    # ...
    
    # TO-DO:
    # Bind cell's on_selection function to popup's self.selection property
    '''
    def __new__(cls, *args, **kwargs):
        print("instance = ", cls.instance)
        if cls.instance is None:
            #FileBrowser.instance = FileBrowser.__FileBrowser()
            print("Calling")
            cls.instance = super(FileBrowser, cls).__new__(cls, *args, **kwargs)#Popup.__new__(cls, *args, **kwargs)
            cls.app = MDApp.get_running_app()
        print("Returing")
        return cls.instance
    def __getattr(self, name):
        return getattr(self.instance, name)
    def __setattr(self, name):
        return setattr(self.instance, name)
    

class Browser(BoxLayout):
    
    browse_btn = Button(text="Browse")
    #browse_btn.bind(on_release=lambda x : x.root.browse(x))
    # bind button to static FileBrowser' browse() function
    browse_btn.bind(on_release=lambda x : FileBrowser.open(FileBrowser.instance))
    text_box = Label(text="...", color=(0,0,0,1))
    
    def __init__(self, **kwargs):
        super(Browser, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.add_widget(self.browse_btn)
        self.add_widget(self.text_box)
    
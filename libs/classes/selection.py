from kivymd.app import MDApp
from kivymd.uix.button import Button
from kivymd.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.graphics import Color, Rectangle


class Selection(Widget):
    
    selection = StringProperty('')
    
    def __init__(self, **kwargs):
        pass
        
    def on_start(self):
        pass
        
    '''
    Using this creattion function to initialize attributes because
    if done from the __init__() function the super's attributes are not
    linked for some reason
    '''
    def __new__(self, *args, **kwargs):
        self.text_box = Label(text="...", color=(0,0,0,1))
        self.layout = BoxLayout(orientation='vertical')
        self.picker_btn = Button(text="Browse")
        self.layout.add_widget(self.picker_btn)
        self.layout.add_widget(self.text_box)
        # Set up background colors
        with self.text_box.canvas.before:
            Color(rbg=(1,1,1) )
            self.text_box.rect = Rectangle(size=self.text_box.size, pos=self.text_box.pos)
        # Bind the background colors location to text_box
        self.text_box.bind(size=self.update_rect, pos=self.update_rect)
        
        inst = super(Selection, self).__new__(self, *args, **kwargs)
        self.layout.root = inst
        return inst
        
    def dismiss(self):
        pass
        
    # Change text_box background color
    def update_rect(self, prop ):
        try:
            self.rect.pos = self.pos
            self.rect.size = self.size
        except Exception as e:
            print(e)
            pass
    
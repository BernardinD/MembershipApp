from kivymd.app import MDApp
from kivymd.uix.button import Button
from kivymd.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.graphics import Color, Rectangle


class Selection(BoxLayout):
    '''The class is used as an class type for things that use some type of selection
    
    Usage:
    When initializing your subclass update the 'text_box' and 'picker_btn'
    to for your specific task
    
    'picket_btn': Button that starts the function of the new subclass
    
    'text_box': The Label that dislays a message, usually of the 
    action of the subclass
    '''
    
    selection = StringProperty('')
    
    def __init__(self, **kwargs):
        print("Before super")
        super(Selection, self).__init__(**kwargs)
        print("After super")
        self.orientation = "vertical"
        self.text_box = Label(text="...", color=(0,0,0,1))
        #self.layout = BoxLayout(orientation='vertical')
        self.picker_btn = Button(text="Browse")
        self.add_widget(self.picker_btn)
        self.add_widget(self.text_box)
        # Set up background colors
        with self.text_box.canvas.before:
            Color(rbg=(1,1,1) )
            self.text_box.rect = Rectangle(size=self.text_box.size, pos=self.text_box.pos)
        # Bind the background colors location to text_box
        self.text_box.bind(size=self.update_rect, pos=self.update_rect)
        
        
    def on_start(self):
        pass
        
    '''
    Using this creattion function to initialize attributes because
    if done from the __init__() function the super's attributes are not
    linked for some reason
    '''
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
        '''
        
    def dismiss(self):
        pass
        
    # Change text_box background color
    #def update_rect(self, caller, val):
    def update_rect(self, text_box, _):
        try:
            text_box.rect.pos = text_box.pos
            text_box.rect.size = text_box.size
        except Exception as e:
            print(e)
            pass
            
    # Change text_box background color size
    def update_rect_size(self, sizeX, sizeY ):
        #print("*args =", *args)
        print("Inside update_rect")
        print("self.text_box.rect.size = ", self.text_box.rect.size)
        try:
            self.text_box.rect.size = (sizeX,sizeY)
        except Exception as e:
            print(e)
            pass
    # Change text_box background color position
    def update_rect_pos(self, posX, posY ):
        #print("*args =", *args)
        print("Inside update_rect")
        print("self.text_box.rect.pos = ", self.text_box.rect.pos)
        try:
            self.text_box.rect.pos = (posX,posY)
        except Exception as e:
            print(e)
            pass
    
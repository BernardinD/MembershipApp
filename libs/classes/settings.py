from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import Button
from kivymd.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.core.clipboard import Clipboard
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from libs.classes.browse import Browser, FileBrowser    # This is for the Label/Button combo object
                                                        # and browser popup, respectively

# All global objects' events are defined in locations where local information is needed
text_box = TextInput(id='txt', multiline=False, halign='center')
browser = Browser(orientation='vertical')
'''browse_btn = Button(text="Browse")
browse_btn.bind(on_release=lambda x : x.root.browse(x))'''

'''class FileBrowser(Popup):
    # Object openning browser
    root = None
    
    def __init__(self, **kwargs):
        super(FileBrowser, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()'''
print("Right before variable")        
fb = FileBrowser()
# Open browsing popup
browser.browse_btn.bind(on_release=fb.open)
print("Right after variable") 

class Change_popup(Popup):

    # Holds current topic
    curr = ""
    
    def __init__(self, **kwargs):
        super(Change_popup, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        text_box.bind(on_text_validate=self.confirm)
    
    def exit(self):
        # Clear placeholder in popup
        self.dismiss()
        self.app.root.ids.settings_id.popup.ids.placeholder.clear_widgets()
        text_box.text = ""
        
    # args = self and MAYBE obj
    def confirm(*args):
        self = args[0]
        # Pribt new and save it to list of settings
        if(self.curr == "Logo"):
            text = browser.text_box.text
        else:
            text = text_box.text
        print("got text")
        self.app.root.ids.settings_id.curr_sett[self.curr] = text
        print(self.app.root.ids.settings_id.ids["logo"].topic)
        for name in self.app.root.ids.settings_id.ids:
            if isinstance(self.app.root.ids.settings_id.ids[name], Settings_cell) and self.app.root.ids.settings_id.ids[name].topic == self.curr:
                self.app.root.ids.settings_id.ids[name].info = text
        self.exit()
    
class Settings_Setup(Screen):
    
    # Holds all the tags that go to editing operations
    changes = ["Current sheet", "Primary color", "Logo"]
    
    # Holds preset values for colors
    colors = {}
    
    def __init__(self, **kwargs):
        super(Settings_Setup, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.popup = Change_popup()
        self.curr_sett = self.app.store.get("Settings")
        
        
    def on_enter(self):
        for name in self.ids:
            if isinstance(self.ids[name], Settings_cell) and self.ids[name].topic in self.app.store.get("Settings"):
                cell = self.ids[name]
                print(cell.ids.button.background_color)
                topic = cell.topic
                info = self.app.store.get("Settings")[cell.topic]
                cell.info = info 
                print("settings.py: **** -----", topic, info, "------------")
                
        
    def save(self):
        saves = dict()
        for name in self.ids:
            if isinstance(self.ids[name], Settings_cell) and self.ids[name].topic in self.changes:
                cell = self.ids[name]
                from kivy.storage.jsonstore import JsonStore
                import os
                store = JsonStore(os.path.join(self.app.abs_root, "assets",'hello.json'))
                topic = str(cell.topic)
                info = str(cell.info)
                print(topic, info)
                #store[""] = {str(topic) : str(info)}
                #store.put("Settings", **{str(topic) : str(info)})
                saves[topic] = info
        store.put("Settings", **saves)
        
class Settings_cell(BoxLayout):
    topic = StringProperty()
    info = StringProperty("'Empty'")
    #btn_color = 

    def __init__(self, **kwargs):
        super(Settings_cell, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        
        # Add in info from json file
        # ...
        
    def change(self):
        root = self.app.root.ids.settings_id
        #root.ids.settings_id.ids.placholder.remove_widget(root.popup.ids.txt)
        # Put current prompt on popup
        if self.topic == "Current sheet":
            root.popup.label = "Enter new sheet's name"
            root.popup.ids.placeholder.add_widget(text_box)
        elif self.topic == 'Primary color':
            root.popup.label = "Enter new color"
        elif self.topic == 'Logo':
            root.popup.label = "Press Browse to find logo"
            fb.bind(selection=self.selection)
            # Make connection to cell, in order to save selection
            #fb.root = self
            browser.browse_btn.root = self
            self.app.root.ids.settings_id.popup.ids.placeholder.add_widget(browser)
        root.popup.curr = self.topic
        root.popup.open()
        text_box.focus = True
        
    def buttons(self):
        if self.topic in self.app.root.ids.settings_id.changes:
            self.change()
        else:
            pass
    
    # Used as retrival function for browser selection
    # A callback for the 'selection' properties in 'fb' and its FileChooser
    def selection(self, obj, val):
        print("in selection")
        browser.text_box.text =  val
        obj.dismiss()
        
    def dismiss(self, selection):
        # Save selection to saves and browse_btn.text, and close popup
        #print(self.root)
        if len(selection) > 0:
            #self.info = selection[0]
            browser.text_box.text=selection[0]
        print("selection =", selection)
        print("self.info =", self.info)
        print("self.topic =", self.topic)
        fb.dismiss()
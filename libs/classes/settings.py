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
from libs.classes.browse import FileBrowser    # This is for the Label/Button combo object
                                                        # and browser popup, respectively

                                                        # For pulling in the widget in 'placeholder'

                
from libs.classes.colorpicker import ColorPicker                
from libs.classes.selection import Selection

import sys


# All global objects' events are defined in locations where local information is needed
text_box = TextInput(id='txt', multiline=False, halign='center')
#browser = Browser(orientation='vertical')

'''class FileBrowser(Popup):
    # Object openning browser
    root = None
    
    def __init__(self, **kwargs):
        super(FileBrowser, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()'''
print("Right before variable")        
#fb = FileBrowser()
# Open browsing popup
#browser.browse_btn.bind(on_release=fb.open)
print("Right after variable") 

class Change_popup(Popup):

    # Holds current topic
    curr = ""
    
    def __init__(self, **kwargs):
        super(Change_popup, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        text_box.bind(on_text_validate=self.confirm)
        self.bind(on_dismiss=self.exit)
     
    # args = self and MAYBE obj
    def confirm(*args):
        self = args[0]
        print("In confirm")
        curr_plc_hldr = self.ids.placeholder.children[0]
        # Print new and save it to list of settings
        
        # If current Op is selecting sheet 
        #(Used for both selection and creation)
        if isinstance(curr_plc_hldr, TextInput):
            text = text_box.text
            
            if (self.curr == "Create new sheet"):
                self.app.root.ids.settings_id.create(text)
                # Change current to 'Current sheet' since the rest of the operation
                #is switch the current sheet
                self.curr = "Current sheet"
                self.app.updates = "Sheet has been created and \n updated as current sheet \n Make sure to save new settings"
                self.app.popup.open()
                
            try:
                sheet = self.app.get_spread(text)
            except:
                self.app.spread_unloaded(MDApp.get_running_app())
                
        # If current Op is for Selection
        #Uses root that was assigned manually to get instance and text_box
        elif curr_plc_hldr.root and isinstance(curr_plc_hldr.root, Selection):
            text = curr_plc_hldr.root.text_box.text
            
        self.app.root.ids.settings_id.curr_sett[self.curr] = text
        
        for name in self.app.root.ids.settings_id.ids:
            if isinstance(self.app.root.ids.settings_id.ids[name], Settings_cell) and self.app.root.ids.settings_id.ids[name].topic == self.curr:
                self.app.root.ids.settings_id.ids[name].info = text
        self.dismiss()
        
    def exit(*args):
        self = args[0]
        # Clear placeholder in popup
        self.app.root.ids.settings_id.popup.ids.placeholder.clear_widgets()
        self.sub = None
        text_box.text = ""
       
    
class Settings_Setup(Screen):
    
    # Holds all the tags that go to editing operations
    changes = ["Current sheet", "Primary color", "Logo"]
    
    # Holds preset values for colors
    colors = {}
    
    def __init__(self, **kwargs):
        super(Settings_Setup, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.popup = Change_popup()
        
        
    '''
    Setting all topics and infos to corresponding cell before stating
    '''
    def on_enter(self):
        # Dictionary of all the settings current set
        self.curr_sett = self.app.store.get("Settings")
        
        # Setting info from json file with correct cell name
        for name in self.ids:
            if isinstance(self.ids[name], Settings_cell) and self.ids[name].topic in self.app.store.get("Settings"):
                cell = self.ids[name]
                print(cell.ids.button.background_color)
                topic = cell.topic
                info = self.app.store.get("Settings")[cell.topic]
                cell.info = info 
                print("settings.py: **** -----", topic, info, "------------")
                
    # Save current settings to json file
    def save(self):
        saves = dict()
        self.app.store.put("Settings", **self.curr_sett)
        self.app.on_back()
        self.app.updates = "Settings have been updated."
        self.app.popup.open()
        
    '''
    Creates a new sheet that is assigned to the email address from  the 'client_secret'
    json file. It is then shared with the club's gmail to transfer ownership
    '''
    def create(self, sheetname = "Test new sheet"):
        # Create new sheet through gspread
        import gspread
        creds = self.app.get_creds()
        client = gspread.authorize(creds)
        
        sh = client.create(sheetname)
        sh.share("bdezius@gmail.com", perm_type='user', role='owner')
        print("New sheet created and shared")


class Settings_cell(BoxLayout):
    '''
    The class for every row of the settings page
    It includes the name of the setting as the 'topic', the data of the setting as the 'info',
    and the button for an action, which is coordinated by the 'buttons' function
    '''
    
    topic = StringProperty()
    info = StringProperty("'Empty'")
    type = StringProperty("'Empty'")
    popup_label = StringProperty("'Empty'")
    
    #btn_color = 

    def __init__(self, **kwargs):
        super(Settings_cell, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.sub = None
        
        # Add in info from json file
        # ...
        
    def str_to_class(self, classname):
        return getattr(sys.modules[__name__], classname)
        
    def change(self):
        '''
        Corrdinates all cells that have to do with changing a setting
        '''
        root = self.app.root.ids.settings_id
        # Put current prompt on popup
        if self.topic == "Current sheet" or self.topic == "Create new sheet":
            root.popup.label = "Enter new sheet's name"
            root.popup.ids.placeholder.add_widget(text_box)
        elif (self.str_to_class(self.type), Selection):
            print("Came in to 'Selection'")
            root.popup.label = self.popup_label
            self.sub = (self.str_to_class(self.type))()
            print("self.sub = ", self.sub)
            self.sub.bind(selection=self.selection)
            self.app.root.ids.settings_id.popup.ids.placeholder.add_widget(self.sub.layout)
            print("selection layout added")
        else:
            print("***** DID NOT GO INTO ANY CASES ******")
        root.popup.curr = self.topic
        root.popup.open()
        text_box.focus = True
        
    def buttons(self):
        '''
        Corrdinates buttons for all cells in page
        '''
        print("**** came into buttons *****")
        #if self.topic in self.app.root.ids.settings_id.changes:
        self.change()
        #elif 'create' in self.topic.lower():
        #    self.app.root.ids.settings_id.create()
        #else:
        #    pass
    
    def selection(self, obj, val):
        '''
        Used as retrival function for Selection class
        A callback for the 'selection' properties
        '''
        print("in selection")
        print("obj = ", obj)
        if self.sub:
            print("self.sub =", self.sub)
        
        # Setting name in selection object
        if not val == "":
            # FileBrowser is the only thing to dismiss currently
            obj.dismiss()
            obj.text_box.text =  val
        
    '''def dismiss(self, selection):
        # Save selection to saves and browse_btn.text, and close popup
        #print(self.root)
        if len(selection) > 0:
            #self.info = selection[0]
            browser.text_box.text=selection[0]
        print("selection =", selection)
        print("self.info =", self.info)
        print("self.topic =", self.topic)
        fb.dismiss()'''
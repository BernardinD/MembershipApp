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
import os


# All global objects' events are defined in locations where local information is needed
text_box = TextInput(id='txt', multiline=False, halign='center')
new_sheet = None

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
         
        # If current Op uses Text Box
        if isinstance(curr_plc_hldr, TextInput):
            text = text_box.text
            if self.curr == "Primary contact":
                pass
                
            # If current Op is selecting sheet
            #(Used for both selection and creation)
            else:
                if (self.curr == "Create new sheet"):
                    try:
                        self.app.root.ids.settings_id.create(text)
                        # Change current to 'Current sheet' since the rest of the operation
                        #is switch the current sheet
                        self.curr = "Current sheet"
                        self.app.updates = "Sheet has been created and \n updated as current sheet \n Make sure to save new settings"
                        self.app.popup.open()
                    except Exception as e:
                        self.app.spread_unloaded()
                        print("settings.py: **** -----", e, "------------")
                        return
                    
                # Setting 'new_sheet' to None after each failed attempted
                #so that any previous successful attempts don't become current
                #sheet.
                # Also returns if sheet doesn't exsist
                global new_sheet
                
                try:
                    new_sheet = self.app.get_spread(text)
                except:
                    self.app.spread_unloaded("name")
                    new_sheet = None
                    return
            
                
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
    '''
    Relys on each cell in the page being broken up into types.
    Mainly there are types that are for directly changing entries, whose
    topics are put into the 'changes' list
    '''
    # Holds all the tags that go to editing operations
    changes = ["Current sheet", "Primary color", "Logo", "Create new sheet",
                "Primary contact"]
    
    # Holds preset values for colors
    colors = {}
    
    def __init__(self, **kwargs):
        super(Settings_Setup, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.popup = Change_popup()
        
    
    def on_enter(self):    
        '''
        Setting all topics and infos to corresponding cell before starting
        '''
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
        '''
        Take current local entries and saved them to json file
        '''
        global new_sheet
        saves = dict()
        self.app.store.put("Settings", **self.curr_sett)
        self.app.logo = self.app.store.get("Settings")["Logo"]
        print("self.app.store.get('Settings') =", self.app.store.get("Settings"))
        self.app.on_back()
        self.app.updates = "Settings have been updated."
        if new_sheet:
            print("---- Sheet is changing ------")
            self.app.sheet = new_sheet
        self.app.popup.open()
     
    def create(self, sheetname = "Test new sheet"):   
        '''
        Creates a new sheet that is assigned to the email address from  the 'client_secret'
        json file. It is then shared with the club's gmail to transfer ownership
        '''
        # Create new sheet through gspread
        import gspread
        creds = self.app.get_creds()
        client = gspread.authorize(creds)
        
        sh = client.create(sheetname)
        email = self.app.store.get("Settings")["Primary contact"]
        sh.share(email, perm_type='user', role='owner')
        global new_sheet
        new_sheet = sh.sheet1
        if "is" == "empty":
            new_sheet.append_row(["First Name", "Last Name", 'Level', "Attendences", "Signed-in", "Email", "Phone #"])
        print("New sheet created and shared")


class Settings_cell(BoxLayout):
    '''
    The class for every row of the settings page
    It includes the name of the setting as the 'topic', the data of the setting as the 'info',
    and the button for an action, which is coordinated by the 'buttons' function
    '''
    
    topic = StringProperty()
    info = StringProperty("'Empty'")
    type = StringProperty("")
    popup_label = StringProperty("'Empty'")
    
    #btn_color = 

    def __init__(self, **kwargs):
        super(Settings_cell, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.sub = None
        
        # Add in info from json file
        # ...
        
    def str_to_class(self, classname):
        # Checks to see if a classname is given. If so, returns the type
        return getattr(sys.modules[__name__], classname) if not (classname == "") else None
        
    def change(self):
        '''
        Corrdinates all cells that have to do with changing a setting
        '''
        root = self.app.root.ids.settings_id
        print("In 'change'")
        cls = self.str_to_class(self.type)
        # Put current prompt on popup
        if cls and issubclass(cls, Selection):
            print("Came in to 'Selection'")
            root.popup.label = self.popup_label
            self.sub = cls()
            print("self.sub = ", self.sub)
            self.sub.bind(selection=self.selection)
            self.app.root.ids.settings_id.popup.ids.placeholder.add_widget(self.sub.layout)
            print("selection layout added")
        else: 
            #self.topic == "Current sheet" or self.topic == "Create new sheet":
            print("In 'change's else")
            root.popup.label = "Enter new sheet's name"
            root.popup.ids.placeholder.add_widget(text_box)
        root.popup.curr = self.topic
        root.popup.open()
        text_box.focus = True
        
    def buttons(self):
        '''
        Corrdinates buttons for all cells in page
        '''
        print("**** came into buttons *****")
        if "Sharing" in self.topic:
            email = self.app.get_creds().service_account_email
            Clipboard.copy(email)
            self.app.alert("App's email account has be copied to clipboard \n Share with pre-exsisting sheet to gain access")
            
        elif self.topic in self.app.root.ids.settings_id.changes:
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
        
    def format_text(self, info, width):
        '''
        Format text so that it fits in Label and looks well-formated.
        It does it by attempting to break up the string by the length 
        of the Label box and print up to 4 lines of text
        '''
        lines = []
        char_width = 7
        width /= char_width
        width = int(width)
        sep = os.sep if os.sep in info else ""
        while len(info) > 0:
            if len(info) < width:
                width = len(info)
            if (info[width-1] == sep):
                width -= 1
            # Splice til length
            temp = info[:width] 
            # Take path up til splice
            split = os.path.split(temp)
            if len(split[0]) > 0:
                lines.append(split[0]+ sep )
                # Reattach rest of spliced path and continue
                if len(split[1]) > 0:
                    info = split[1] + info[width:]
            else:
                # Check if part if remaining path is too long (first part of split will be empty)
                split2 = (split[1] + info[width:]).split(os.sep)
                if len(split2) > 1 or len(lines) > 4:
                    lines = [
                        "** - Path had to be cropped - **",
                        " ",
                        "... "+info[-(width- (char_width*3)) : ]
                    ]
                    break
                lines.append(split[1])
                info = ""
        text = "\n".join(lines)
        return text
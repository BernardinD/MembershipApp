#!/usr/bin/env python3
#import validators
try:
    import sys
    import os
    
    # Assuming executable/script to be at head or 'dist'
    abs_root = os.path.split(os.path.abspath("."))[0]
    if "PusloMembershipApp" not in abs_root:
        abs_root = os.path.join(abs_root, "PusloMembershipApp")
        
    if getattr(sys, "frozen", False):  # bundle mode with PyInstaller
        os.environ["PULSO_APP_ROOT"] = sys._MEIPASS
    else:
        sys.path.append(os.path.abspath(__file__).split("demos")[0])
        os.environ["PULSO_APP_ROOT"] = os.path.dirname(os.path.abspath(__file__))
    os.environ["PULSO_APP_ASSETS"] = os.path.join(
        os.environ["PULSO_APP_ROOT"], f"assets{os.sep}"
    )
    print('os.environ["PULSO_APP_ROOT"] =', os.environ["PULSO_APP_ROOT"])
    print('os.environ["PULSO_APP_ASSETS"] =', os.environ["PULSO_APP_ASSETS"])
    from kivy_garden.zbarcam import ZBarCam
    from kivy_garden import zbarcam 
    temp_path = os.path.abspath(zbarcam.__file__)
    temp_path = temp_path.split("zbarcam")[0]
    print("temp_path = ", temp_path)
    import glob
    from os.path import join
    from os import sep
    for file in glob.iglob(join("**{}*".format(sep)), recursive=True):
        print (file)
        
    sys.path.insert(0, temp_path)
    from kivy_deps import sdl2, glew
    from kivymd import hooks_path as kivymd_hooks_path
    from kivy.lang import Builder
    from kivy.utils import platform
    print('os.path.abspath(".") =', os.path.abspath("."))
    #from kivy.utils import platform
    if platform in 'win,linux':
        from kivy_garden.qrcode import QRCodeWidget
        Builder.load_file(os.path.join(
                    os.environ["PULSO_APP_ROOT"], "libs", "kv",
                    "add_memb.kv"))
    
    Builder.load_file(os.path.join(
                os.environ["PULSO_APP_ROOT"], "libs", "kv",
                "settings.kv"))
    Builder.load_file(os.path.join(
                os.environ["PULSO_APP_ROOT"], "libs", "kv",
                "browse.kv"))
    Builder.load_file(os.path.join(
                os.environ["PULSO_APP_ROOT"], "libs", "kv",
                "home.kv"))
    Builder.load_file(os.path.join(
                os.environ["PULSO_APP_ROOT"], "libs", "kv",
                "colorpicker.kv"))
    Builder.load_file(os.path.join(
                os.environ["PULSO_APP_ROOT"], "libs", "kv",
                "selection.kv"))
    from kivymd.app import MDApp
    from kivy.clock import Clock
    #from kivy.core.clipboard import Clipboard
    from kivy.logger import LOG_LEVELS, Logger
    from kivy.properties import StringProperty, BooleanProperty, NumericProperty
    from kivy.uix.screenmanager import Screen, ScreenManager
    from kivymd.icon_definitions import md_icons
    from kivymd.theming import ThemeManager
    from kivymd.uix.toolbar import MDToolbar
    from kivy.graphics import Color, Rectangle
    from kivymd.uix.button import Button
    from kivymd.uix.label import Label
    from kivy.uix.boxlayout import BoxLayout
    from kivymd.uix.list import OneLineAvatarListItem
    from kivy.uix.popup import Popup
    from kivymd.uix.navigationdrawer import MDNavigationDrawer
    from libs.classes.settings import Settings_Setup
    from libs.classes.home import Home
    #/////////////////////////////////////
    
    from kivy.storage.jsonstore import JsonStore

    #store = JsonStore(os.path.join(abs_root, "assets",'settings.json'))
    #print('store.get("Settings")["Current sheet"] =', store.get("Settings")["Current sheet"] if 'Current sheet' in store else None)
    
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials

    
    #sheet = None

        
    # Try to get spread sheet
    #try:
    #    sheet = get_spread()
    #except:
    #    pass

    levels = {'Beginner':(1, 0, 0, 1), 'Intermediate':(0, 0, 1, 1), "Advanced":(1, 1, 0, 1)}
    from plyer import email
    #///////////////////////////////////

    from kivy.core.window import Window

    class CustomToolbar(MDToolbar):
        """
        Toolbar with helper method for loading default/back buttons.
        """
        
        state = BooleanProperty()
        
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            Clock.schedule_once(self.load_default_buttons)
            self.app = MDApp.get_running_app()

        def on_state(self, *args):
            if self.app.root.ids.nav_drawer.state == "close":
                self.left_action_items = [['menu', lambda x: self.toggle_state()]]
            elif self.app.root.ids.nav_drawer.state == "open":
                self.left_action_items = [['arrow-right', lambda x: self.toggle_state()]]

        def load_default_buttons(self, dt=None):
            app = MDApp.get_running_app()
            #self.left_action_items = [
            #    ['menu', lambda x: app.root.set_state("toggle")]]
            self.right_action_items = [
                ['dots-vertical', lambda x: self.app.root.toggle_nav_drawer()]]

        def load_back_button(self, function):
            self.left_action_items = [['arrow-left', lambda x: function()]]
            
    class Scan(Screen):
        
        def __init__(self, **kwargs):
            #self.manager = manager
            super(Scan, self).__init__(**kwargs)
            self.screen = False
            self.app = MDApp.get_running_app()

        def _after_init(self, dt):
            """
            Turns off ZBarCam until needed
            """
            #self.ids['zbarcam'].stop()
            
        def scanned(self):
            """
            A function executed when a qrcode is detected.
            """
            # The on_symbols event is also fired when list gets empty, then it would raise an IndexError
            if self.ids.zbarcam.symbols and self.screen:
                symbol = self.ids.zbarcam.symbols[0]
                data = symbol.data.decode('utf8')
                print(data)
                if self.app.club_striped in data:
                    temp = data.split(',')
                    if len(temp) < 2:
                        return
                    qrfound_screen = self.app.changeScreen('drive_screen')
                        
                    if qrfound_screen:
                        qrfound_screen.data_property = data
                
        def on_enter(self):
            #self.ids['zbarcam'].start()
            self.screen = True
        def on_pre_leave(self):
            #self.ids['zbarcam'].stop()
            self.screen = False
                
    class Drive(Screen):

        data_property = StringProperty()

        prompt_property = StringProperty()
        col_property = NumericProperty()
        flag_property = BooleanProperty() # Defaults to True
        
        def __init__(self, **kwargs):
            #self.manager = manager
            #self.symbol = ''
            self.row = None
            super(Drive, self).__init__(**kwargs)
            self.prompt_property = 'Would you like sign this person in?'
            self.col_property = 5
            self.app = MDApp.get_running_app()
            
        
        def on_flag_property(self, instance, val):
            # True -> sign in; False -> test out
            if val:
                self.col_property = 5
                self.prompt_property = 'Would you like sign this person in?'
                self.app.root.ids['home_id'].ids['scan_button'].text = "Sign in"
                # Popup for  switch between Sign-in/Test-out
                self.app.updates = "Scanner now set to Sign In"
                self.app.popup.open()
            else:
                self.col_property = 3
                self.prompt_property = "Test out?"
                self.app.root.ids['home_id'].ids['scan_button'].text = "Test out"
                # Popup for  switch between Sign-in/Test-out
                self.app.updates =  "Scanner now set to Test out"
                self.app.popup.open()
                
            self.app.root.ids.nav_drawer.set_state("close")
                
                
        def on_data_property(self, instance, value):
            """
            Updates `icon_property` and `title_property`.
            """
            temp = value.split(',')
            first_name = temp[1].strip()
            last_name = temp[2].strip()
            first_names = self.app.sheet.findall(first_name)
            last_names = self.app.sheet.findall(last_name)
            row = None
            levels_obj=self.ids['level']
            print("testing ->", first_names)
            print("testing ->", last_names)
            # Find matching row and column
            for name in first_names:
                for lname in last_names:
                    if name.row == lname.row:
                        row = name.row
                        level = self.app.sheet.cell(row, 3).value
                        print("row = ", row)
                        self.ids['name'].text = "{} {}".format(first_name, last_name)
                        # If member not currently signed in -> normal behavior, else -> print as message
                        levels_obj.text = ("{}".format(level)) if ('No' in self.app.sheet.cell(row, 5).value) or self.col_property == 3  else 'Already signed in.'
                        levels_obj.background_color = (levels[level]) if ('No' in self.app.sheet.cell(row, 5).value) or self.col_property == 3  else (0,0,0,1)
                        # Disable sign-in if already signed in
                        print("******* Here")
                        self.ids['yes'].disabled = False if ('No' in self.app.sheet.cell(row, 5).value) or self.col_property == 3 else True
                        self.row = row
                        return
            self.ids['name'].text = "User not found."
            self.ids['level'].text = "..."
            self.ids['yes'].disabled = True
            levels_obj.background_color = (0,0,0,1)
        
        def approve(self):
            # Change 'Signed in' to 'Yes'
            self.app.sheet.update_cell(self.row, self.col_property, 'Yes' if (self.col_property == 5) else self.getNextLevel())
            print(self.app.sheet.get_all_values())
            # Call 'cancel()' since all it does it return to home
            self.cancel()
            
        def getNextLevel(self):
            curr_level = list(levels.keys()).index(self.ids['level'].text)
            return list(levels.keys())[curr_level+1] if curr_level+1 < len( (levels.keys()) ) else list(levels.keys())[curr_level]
            
        def cancel(self):
            self.app.on_back()
            
    class ContentNavigationDrawer(BoxLayout):
        def __init__(self, **kwargs):
            super(ContentNavigationDrawer, self).__init__(**kwargs)
            self.app = MDApp.get_running_app()
            


    class AddMember(Screen):
       
        def __init__(self, **kwargs):
            super(AddMember, self).__init__(**kwargs)
            self.app = MDApp.get_running_app()
            
        '''def go_home(self):
            self.app.changeScreen('home_screen')'''

        def on_pre_enter(self):
            self.ids['intent_button'].disabled = False
            self.ids['first_name'].text = ''
            self.ids['last_name'].text = ''
            self.ids['mem_email'].text = ''
            self.ids['mem_phone'].text = ''
            self.ids['confirm_button'].disabled = True
            self.ids['again_button'].disabled = True
            self.ids['home_button'].disabled = True
            
        
        def add_member(self, button, first_name, last_name, email, phone):
            # Create QR Code
            print(self.ids['testing'].text)
            creds = self.app.get_creds()
            if creds.access_token_expired:
                try:
                    self.app.sheet = get_spread()
                except:
                    self.app.spread_unloaded()
                    
            self.app.sheet.append_row([first_name.strip(),last_name.strip(), 'Beginner', 0, 'No', email, phone])
            button.disabled = True
            self.ids['home_button'].disabled = False
            self.ids['again_button'].disabled = False
            self.ids['qr'].data = "{},{},{}".format(self.app.club_striped,first_name,last_name)

        def confirm(self, button):
            button.disabled = True
            self.ids['confirm_button'].disabled = False
        
        pass
            
    class NavigationItem(OneLineAvatarListItem):
        icon = StringProperty()
        idx = NumericProperty()
            
        def __init__(self, **kwargs):
            super(NavigationItem, self).__init__(**kwargs)
            self.app = MDApp.get_running_app()
        def home(self):
            self.app.toggle_nav_drawer()
            
        def reload(self):
            try:
                # Reload google self.app.sheet
                self.app.sheet = self.app.get_spread()
                self.app.root.ids.nav_drawer.set_state("toggle")
                # Popup for  switch between Sign-in/Test-out
                self.app.updates = "Members have been reloaded"
                self.app.popup.open()
            except:
                self.app.spread_unloaded()
            
        def settings(self):
            # Change Google sheet
            self.app.changeScreen('settings_screen')
            self.app.root.ids.nav_drawer.set_state("toggle")
            pass
            
        def exit(self):
            self.app.exit()
            
        def __init__(self, index=0, **kwargs):
            super().__init__(**kwargs)
            self.idx = index
            self.switcher = {
                #1:self.switch,
                2:self.reload,
                3:self.settings,
                4:self.exit
            }
            self.app = MDApp.get_running_app()
            
            '''if index == 2:
                content = BoxLayout(orientation='vertical')
                label = Label(text="Members have been reloaded", size_hint=(1,0.5))
                button=Button(text="OK", size_hint=(1,0.5))
                content.add_widget(label)
                content.add_widget(button)
                self.popup = Popup(title="Update",
                        content=content, 
                        size_hint=(.3, .3),
                        auto_dismiss=True)
                button.bind(on_release=self.popup.dismiss)'''
            
        def pressed(self):
            func = self.switcher.get(self.idx, lambda: "Invalid Function")
            func()
        
        
    class MainApp(MDApp):

        updates = StringProperty("Members have been reloaded")
        logo = StringProperty("")
        
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            Window.bind(on_keyboard=self.on_key)
            self.app = MDApp.get_running_app()
            self.screen_list = []
            self.nav_state = False
            self.store = JsonStore(os.path.join(abs_root, "assets",'settings.json'))
            #print("self.store.get('Settings') = ", self.store.get("Settings") )
            #print('self.store.get("Settings")["Current sheet"] =', self.store.get("Settings")["Current sheet"] if 'Current sheet' in self.store.get("Settings") else None)
            self.abs_root = abs_root
            self.logo = self.store.get("Settings")["Logo"]
            self.club_striped = self.strip_name()
            
            #Used for global sheet manipulation
            self.sheet = None
            
            # Try to get sheet if accessable. Already handling the situation
            #where no sheet is loaded later in 'on_start' and 'changeScreen'
            try:\
                self.sheet = self.get_spread()
            except Exception as e:
                print(e)
                pass
            
            # Popup used for updates
            content = BoxLayout(orientation='vertical')
            label = Label(text=self.updates, size_hint=(1,0.5), id="updates", halign='center')
            self.bind(updates=label.setter('text'))
            button=Button(text="OK", size_hint=(1,0.5))
            content.add_widget(label)
            content.add_widget(button)
            self.popup = Popup(title="Update",
                    content=content, 
                    size_hint=(.3, .3),
                    auto_dismiss=True)
            button.bind(on_release=self.popup.dismiss)

        def on_key(self, window, key, *args):
        
            if key == 27:  # the esc key
                print("main.py: ********* in on_key*********")
                print("main.py: ********* screen_list = ", self.screen_list, "*******")
                # If nav is open or on a sub-screen
                if self.screen_list:
                    # If nav drawer is open, make sure to close it
                    if self.screen_list:
                        self.on_back();
                    return True
                else:
                    self.app.exit()
                    return True
            return False
            
        def on_back(self):
            self.root.ids.screen_manager_id.transition.direction = 'right'
            self.root.ids.screen_manager_id.current = self.screen_list.pop()
        
        def on_start(self):
            # The numbers in the list of tuples refer to the operations in the 
            # NavigationItem under 'switcher'
            for items in [
                #("home-circle-outline", "Home",1),
                ("update", "Reload Members",2),
                ("settings-outline", "Open Settings",3),
                ("exit-to-app", "Exit",4),
            ]:
                self.root.ids.content_drawer.ids.box_item.add_widget(
                    NavigationItem(
                        items[2],
                        text=items[1],
                        icon=items[0],
                    )
                )
            #self.root.ids.nav_drawer.bind(state=self.toggle_nav_drawer)
            
            # Make sure sheet is ready before starting normal operation
            if not self.sheet:
                print("In from of popup")
                self.spread_unloaded()
            
        def strip_name(self):
            club = self.app.store.get("Settings")["Club name"]
            club_striped = ''.join(e for e in club if e.isalnum())
            return club_striped
            
        def changeScreen(self, next):
            # To make sure spreadsheet is loaded
            if not self.sheet  and not(next == "settings_screen"):
                self.spread_unloaded()
                return None
                
            if self.root.ids.screen_manager_id.current not in self.screen_list:
                self.screen_list.append(self.root.ids.screen_manager_id.current)
                
            self.root.ids.screen_manager_id.transition.direction = 'left'
            self.root.ids.screen_manager_id.current = next
            
            return self.root.ids.screen_manager_id.current_screen
            
        def get_creds(self):
            scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
            if 'client_secret.json' not in os.listdir(os.environ["PULSO_APP_ASSETS"]):
                print("sys.path =", sys.path)
                dirs = [ i for i in sys.path if os.path.isdir(i)]
                for i in dirs:
                    print("listdir(i) =", os.listdir(i))
                    #print(os.listdir("C:\\Users"))
                    try:
                        if 'client_secret.json' in os.listdir(i):
                            print("Trying to get json")
                            creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(i,'client_secret.json'), scope)
                            break
                        # If can't find json, end program
                    except Exception as e:
                        print(e)
                print("---- Didn't find json ----")
                print("---- Terminating application ----")
                raise True
            else:
                creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(
                                                                            os.environ["PULSO_APP_ASSETS"],
                                                                            'client_secret.json'),
                                                                        scope)
            return creds
            
        
        
        def get_spread(self, sheet = None):
            '''
            Used to retrieve sheets and check if a sheet exists,
            returns the sheet if it exists/accessable
            '''
            if not sheet:
                sheet = self.store.get("Settings")["Current sheet"]
                
            creds = self.get_creds()
            client = gspread.authorize(creds)
            print("Sheet name =", sheet)
            sheet = client.open( sheet ).sheet1
            print("sheet =", sheet)
            print("sheet =", sheet.get_all_values())
            return sheet
            
        def spread_unloaded(self, type_ = "connection"):
            self.app.updates = "Spreadsheet could not be loaded.\nCheck {} and reload".format(type_)
            self.app.popup.open()
            
        def exit(self):
            print("main.py: ********* self.exit run *****")
            app = MDApp.get_running_app()
            app.root.ids.scan_id.ids.zbarcam.stop()
            try:
                app.stop()
            except Exception as e:
                print(e)
                pass
            print("main.py: ********* STOPPED ******")
            
        def build(self):
            self.icon = "docs/images/icon.png"
            
            # Return main root
            return Builder.load_file(os.path.join(
                    os.environ["PULSO_APP_ROOT"], "libs", "kv",
                    "main.kv"))

        def alert(self, mess):
            self.updates = mess
            self.popup.open()

    def main():
        # when the -d/--debug flag is set, Kivy sets log level to debug
        level = Logger.getEffectiveLevel()
        in_debug = level == LOG_LEVELS.get('debug')
        #client = configure_sentry(in_debug)
                
        MainApp().run()


    if __name__ == '__main__':
        main()
except Exception as e:
    print(e)
    input("Application crashed.\nPress 'Enter/Return' to close")
    if isinstance(e, TypeError):
        print("main.py: ********* came in ******")
        pass
    
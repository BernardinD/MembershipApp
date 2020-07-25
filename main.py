#!/usr/bin/env python3
#import validators
try:
    import sys
    import os
    from os.path import join
    from os import sep
    from kivy.logger import Logger
    
    # ////// Setting up requried paths //////////
    # Assuming executable/script to be at head or 'dist'
    abs_root = os.path.split(os.path.abspath("."))[0]
    if "MembershipApp" not in abs_root:
        abs_root = os.path.join(abs_root, "MembershipApp")
        
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
    # ////////////////////////////////////////////
    
    # ///////////// Loading my classes ///////////
    from libs.classes.home import Home
    from libs.classes.scan import Scan
    from libs.classes.verify import Verify
    # ////////////////////////////////////////////
    
    # //////////// Loading in designs ////////////
    from kivy.lang import Builder
    from kivy.utils import platform
    print('os.path.abspath(".") =', os.path.abspath("."))
    # Only load in 'add_memb' design if on a PC
    if platform in 'win,linux':
        Logger.info("ALERT: Running on PC")
        from libs.classes.add_memb import AddMember
        from kivy_garden.qrcode import QRCodeWidget
        Builder.load_file(os.path.join(
                    os.environ["PULSO_APP_ROOT"], "libs", "kv",
                    "add_memb.kv"))
    
    Builder.load_file(os.path.join(
                os.environ["PULSO_APP_ROOT"], "libs", "kv",
                "settings.kv"))
    Builder.load_file(os.path.join(
                os.environ["PULSO_APP_ROOT"], "libs", "kv",
                "scan.kv"))
    Builder.load_file(os.path.join(
                os.environ["PULSO_APP_ROOT"], "libs", "kv",
                "verify.kv"))
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
    # ////////////////////////////////////////////
    
    # ////////// Kivy libraries/classes //////////
    from kivymd.app import MDApp
    from kivy.clock import Clock
    from kivy.logger import LOG_LEVELS, Logger
    from kivy.properties import StringProperty, BooleanProperty, NumericProperty
    from kivy.uix.screenmanager import Screen, ScreenManager
    from kivymd.uix.toolbar import MDToolbar
    from kivy.graphics import Color, Rectangle
    from kivymd.uix.button import Button
    from kivymd.uix.label import Label
    from kivy.uix.boxlayout import BoxLayout
    from kivymd.uix.list import OneLineAvatarListItem
    from kivy.uix.popup import Popup
    from kivymd.uix.navigationdrawer import MDNavigationDrawer
    from libs.classes.settings import Settings_Setup
    from kivy.core.window import Window
    from kivy.storage.jsonstore import JsonStore
    # ////////////////////////////////////////////
    
    # ///////////// GSpread Essentials ////////////
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    #/////////////////////////////////////////////

    # Club membership levels
    levels = {'Beginner':(1, 0, 0, 1), 'Intermediate':(0, 0, 1, 1), "Advanced":(1, 1, 0, 1)}
            
    class ContentNavigationDrawer(BoxLayout):
        def __init__(self, **kwargs):
            super(ContentNavigationDrawer, self).__init__(**kwargs)
            self.app = MDApp.get_running_app()
            
    class NavigationItem(OneLineAvatarListItem):
        '''Creates an object for every item in the side-menu
        ...
        >>> NavigationItem(menu_idx, setting_txt, icon)
        
        Icon names can be found at: https://github.com/HeaTTheatR/KivyMD/blob/master/kivymd/icon_definitions.py
        '''
        icon = StringProperty()
        idx = NumericProperty()
        
        # List of all the operations in the menu
        switcher = {}
            
        '''def __init__(self, **kwargs):
            super(NavigationItem, self).__init__(**kwargs)
            self.app = MDApp.get_running_app()'''
                
        def __init__(self, index=0, **kwargs):
            super().__init__(**kwargs)
            self.app = MDApp.get_running_app()
            
            self.idx = index
            self.switcher = {
                #1:self.switch,
                2:self.reload,
                3:self.settings,
                4:self.exit
            }
            
        def reload(self):
            '''
            Reloads spreadsheet
            '''
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
            '''
            Goes to settings page
            '''
            self.app.changeScreen('settings_screen')
            self.app.root.ids.nav_drawer.set_state("toggle")
            pass
            
        def exit(self):
            self.app.exit()
            
        def pressed(self):
            func = self.switcher.get(self.idx, lambda: "Invalid Function")
            func()
        
        
    class MainApp(MDApp):

        # Prompt for popup alert box
        updates = StringProperty("Members have been reloaded")
        
        # String for path of club logo 
        logo = StringProperty("")
        
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            Window.bind(on_keyboard=self.on_key)
            self.app = MDApp.get_running_app()
            self.screen_list = []
            self.nav_state = False
            self.store = JsonStore(os.path.join(abs_root, "assets",'settings.json'))
            self.abs_root = abs_root
            self.logo = self.store.get("Settings")["Logo"]
            self.club_striped = self.strip_name()
            self.levels = levels
            
            #Used for global sheet manipulation
            self.sheet = None
            
            # Try to get sheet if accessable. Already handling the situation
            #where no sheet is loaded later in 'on_start' and 'changeScreen'
            try:
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
            '''
            Handles the esc button on PC and 'back' on android
            Must return True to stop the stack of the key press
            '''
            
            if key == 27:
                #print("main.py: ********* in on_key*********")
                #print("main.py: ********* screen_list = ", self.screen_list, "*******")
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
            '''
            Removes all special special characters and spaces from club name
            '''
            club = self.app.store.get("Settings")["Club name"]
            club_striped = ''.join(e for e in club if e.isalnum())
            return club_striped
            
        def changeScreen(self, next):
            '''
            Handles all the changing of screens
            '''
            # To make sure spreadsheet is loaded
            if not self.sheet  and not(next == "settings_screen"):
                self.spread_unloaded()
                return None
                
            current= self.root.ids.screen_manager_id.current
            if current not in self.screen_list and current not in next:
                print("Added new screen to list")
                self.screen_list.append(self.root.ids.screen_manager_id.current)
                
                self.root.ids.screen_manager_id.transition.direction = 'left'
                self.root.ids.screen_manager_id.current = next
            
            return self.root.ids.screen_manager_id.current_screen
            
        def get_creds(self):
            '''
            Get the credentials to access the spreadsheet
            '''
            
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
            app = MDApp.get_running_app()
            app.root.ids.scan_id.ids.zbarcam.stop()
            app.stop()
            
        def build(self):
            self.icon = "docs/images/icon.png"
            
            # Return main root
            return Builder.load_file(os.path.join(
                    os.environ["PULSO_APP_ROOT"], "libs", "kv",
                    "main.kv"))

        def alert(self, mess):
            '''
            Displays popup for alert messages
            '''
            
            # Check if this Popup is already open
            for wid in self.app.get_running_app().root_window.children:
                if wid == self.popup:
                    print("main.py: **** ----- More than one alert has been fire ------------")
                    print("main.py: **** ----- {} ------------".format(mess))
                    return
            
            self.updates = mess
            self.popup.open()

    def main():
        # when the -d/--debug flag is set, Kivy sets log level to debug
        level = Logger.getEffectiveLevel()
        in_debug = level == LOG_LEVELS.get('debug')
        
        reset()
        MainApp().run()

    def reset():
        '''
        Prevents the 'TypeError' that sometimes happens
        '''
        
        import kivy.core.window as window
        from kivy.base import EventLoop
        if not EventLoop.event_listeners:
            from kivy.cache import Cache
            window.Window = window.core_select_lib('window', window.window_impl, True)
            Cache.print_usage()
            for cat in Cache._categories:
                Cache._objects[cat] = {}
                
                
    if __name__ == '__main__':
        main()
except Exception as e:
    print(e)
    input("Application crashed.\nPress 'Enter/Return' to close")
    
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
    abs_root = os.path.abspath(".")
    print("abs_root = ", abs_root)
    print("files=", os.listdir("."), sep='\n')
    print("./assets = ", os.listdir("./assets") )
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
    from libs.classes.add_memb import AddMember
    # ////////////////////////////////////////////
    
    # //////////// Loading in designs ////////////
    from kivy.lang import Builder
    from kivy.utils import platform
    print('os.path.abspath(".") =', os.path.abspath("."))
    # Only load in 'add_memb' design if on a PC
    if platform in 'win,linux':
        Logger.info("ALERT: Running on PC")
        if "MembershipApp" not in abs_root:
            abs_root = os.path.join(abs_root, "MembershipApp")
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
    from google.oauth2 import service_account
    #/////////////////////////////////////////////

    # Club membership levels
    levels = {'Beginner':(1, 0, 0, 1), 'Intermediate':(0, 0, 1, 1), "Advanced":(1, 1, 0, 1)}
            
    class ContentNavigationDrawer(BoxLayout):
        def __init__(self, **kwargs):
            super(ContentNavigationDrawer, self).__init__(**kwargs)
            self.app = MDApp.get_running_app()
            
    class NavigationItem(OneLineAvatarListItem):
        ''' Creates an object for every item in the side-menu
        
        Usage:
        >>> NavigationItem(menu_idx, setting_txt, icon)
        
        Icon names can be found at: https://github.com/HeaTTheatR/KivyMD/blob/master/kivymd/icon_definitions.py
        '''
        icon = StringProperty()
        idx = NumericProperty()
        
        # List of all the operations in the menu
        switcher = {}
            
                
        def __init__(self, index=0, **kwargs):
            super().__init__(**kwargs)
            self.app = MDApp.get_running_app()
            
            self.idx = index
            self.switcher = {
                1:self.reload,
                2:self.settings,
                3:self.exit
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
            Changes screen to settings page
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
            
            # Create folder
            from googleapiclient.discovery import build
            drive_service = build(u'drive', u'v3', credentials=self.get_creds())
            
            '''
            file_metadata = {
                'name': "Test",
                'mimeType': 'application/vnd.google-apps.folder'
            }
            file = drive_service.files().create(body=file_metadata,
                                                fields='id').execute()
            file_metadata = {
                'name': "Testy",
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [file.get('id')]
            }
            file = drive_service.files().create(body=file_metadata,
                                                fields='id').execute()
            file_metadata = {
                'name': "Testytest",
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [file.get('id')]
            }
            file = drive_service.files().create(body=file_metadata,
                                                fields='id').execute()
            file_metadata = {
                'name': "Invoices",
                'mimeType': 'application/vnd.google-apps.folder',
                #'parent': [file.get('id')]
            }
            file = drive_service.files().create(body=file_metadata,
                                                fields='id').execute()
            '''
            
            '''
            if self.find_folders(drive_service, 'Test', 'Test'):
                print("--- Found Folder.")
            else:
                print("--- Folder not found.")
            '''
                
            # Try to get sheet if accessable. Already handling the situation
            #where no sheet is loaded later in 'on_start' and 'changeScreen'
            try:
                self.sheet = self.get_spread()
                
                
                # Create folder for sheet if needed
                self.create_folders()
                
            except Exception as e:
                print(e)
                pass
            
            # Popup used for updates
            content = BoxLayout(orientation='vertical')
            label = Label(text=self.updates, size_hint=(1,0.5), halign='center', font_size='15sp')
            self.bind(updates=label.setter('text'))
            button=Button(text="OK", size_hint=(1,0.5))
            content.add_widget(label)
            content.add_widget(button)
            size_hint = (.3,.3) if platform in 'win,linux' else (.6,.3)
            self.popup = Popup(title="Update",
                    content=content, 
                    size_hint=size_hint,
                    auto_dismiss=True)
            button.bind(on_release=self.popup.dismiss)

        def on_key(self, window, key, *args):
            '''
            Handles the esc button on PC and 'back' on android
            Must return True to stop the stack of the key press
            '''
            
            if key == 27:
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
                ("update", "Reload Members",1),
                ("settings-outline", "Open Settings",2),
                ("exit-to-app", "Exit",3),
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
            
            scope = ["https://www.googleapis.com/auth/spreadsheets", 
                        "https://www.googleapis.com/auth/drive", 
                        "https://www.googleapis.com/auth/drive.file",
                    ]
            
            # Find credentials json file and make connection
            if 'client_secret.json' not in os.listdir(os.environ["PULSO_APP_ASSETS"]):
                print("sys.path =", sys.path)
                dirs = [ i for i in sys.path if os.path.isdir(i)]
                for i in dirs:
                    print("listdir(i) =", os.listdir(i))
                    #print(os.listdir("C:\\Users"))
                    try:
                        if 'client_secret.json' in os.listdir(i):
                            print("Trying to get json")
                            #creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(i,'client_secret.json'), scope)
                            credentials = service_account.Credentials.from_service_account_file(os.path.join(i,'client_secret.json'), scopes=scope)
                            break
                        # If can't find json, end program
                    except Exception as e:
                        print(e)
                print("---- Didn't find json ----")
                print("---- Terminating application ----")
            else:
                #creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(
                #                                                            os.environ["PULSO_APP_ASSETS"],
                #                                                            'client_secret.json'),
                #                                                        scope)
            
                credentials = service_account.Credentials.from_service_account_file(
                        os.path.join(
                            os.environ["PULSO_APP_ASSETS"],
                            'client_secret.json'), scopes=scope)
            return credentials
            
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
            print("sheet.url =", sheet.url)
            print("sheet.id =", sheet.url.split('/')[-1])
            return sheet
            
        def spread_unloaded(self, type_ = "connection"):
            self.app.updates = "Spreadsheet could not be loaded.\nCheck {} and reload".format(type_)
            self.app.popup.open()
            
        def find_folders(self, drive_service, parent, sub=None):
            ''' Returns the folder object or its subfolder if it exists
            '''
            response = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                                  spaces='drive',
                                                  fields='nextPageToken, files(id, name, webViewLink, parents)',
                                                  ).execute()
                                                  
            for file in response.get('files', []):
                # Process change
                print ('Found file: %s (%s)' % (file.get('name'), file.get('id')) )
                print ('parents: ', file.get('parents'))
                print(file.get('webViewLink'))
                
                if parent == file.get('name'):
                    parent = file
                    break
            else:
                return None,None
                
            if sub:
                response = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder' and \
                                                        name = '{}' and \
                                                        '{}' in parents".format( sub, parent.get('id'), ),
                                                      spaces='drive',
                                                      fields='nextPageToken, files(id, name, webViewLink, parents)',
                                                      ).execute()
                if response.get('files', []):
                    sub = response.get('files', [])[0]
                else:
                    sub = None
                
            return parent,file
            
        def create_folders(self):
            from googleapiclient.discovery import build
            drive_service = build(u'drive', u'v3', credentials=self.get_creds())
                                              
            from datetime import date
            names = [self.store.get("Settings")["Current sheet"], '{}'.format(date.today().year)]
            folders = self.find_folders(drive_service, names[0], names[1])
            print("--- Folders searched")
                                              
            prevID = "root"
            for folder, name in zip(folders,names):
                if not folder:
                    # Create folder
                    print("--- Creating folder.")
                    file_metadata = {
                        'name': name,
                        'mimeType': 'application/vnd.google-apps.folder',
                        'parents': [prevID]
                    }
                    folder = drive_service.files().create(body=file_metadata,
                                                        fields='id').execute()
                    print ( 'Folder ID: %s' % folder.get('id') )
                    
                    # Share folder with club email
                    user_permission = {
                        'type': 'user',
                        'role': 'Owner',
                        'emailAddress': self.app.store.get("Settings")["Primary contact"]
                    }
                    drive_service.permissions().create(
                        fileId=folder.get('id'),
                        body=user_permission,
                        fields='id',
                        transferOwnership='true', 
                    ).execute()
                prevID = folder.get('id')
            
        def exit(self):
            app = MDApp.get_running_app()
            
            '''
            from googleapiclient.discovery import build
            file_metadata = {
                'name': 'Invoices',
                'mimeType': 'application/vnd.google-apps.folder'
            }
            drive_service = build(u'drive', u'v3', credentials=self.get_creds())
            
            response = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                                  spaces='drive',
                                                  fields='nextPageToken, files(id, name, webViewLink, parents, owners)',
                                                  ).execute()
            for file in response.get('files', []):
                # Process change
                print ('Found file: %s (%s)' % (file.get('name'), file.get('id')) )
                print ('parents: ', file.get('parents'))
                print('webViewLink: ', file.get('webViewLink'))
                
                #if 'Invoices' in file.get('name') :
                if file.get('owners')[0]['me']:
                    response = drive_service.files().delete(fileId=file.get('id')).execute()
                    print("response =", response)
            '''
            
            app.root.ids.scan_id.ids.zbarcam.stop()
            self.app.stop()
            print("Did something after")
            
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
        print("Returned from run")
        #reset()

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
    

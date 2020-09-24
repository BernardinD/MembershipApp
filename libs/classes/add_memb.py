from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.graphics.instructions import Callback
from libs.send_email import create_message_with_attachment as create_email
from libs.send_email import send_message as send_email

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

import webbrowser
import re
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

import cv2
import numpy as np

class AddMember(Screen):
   
    def __init__(self, **kwargs):
        super(AddMember, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        
        self.service = build('gmail', 'v1', credentials=self.app.get_creds())
        
        #Clock.schedule_once(self.init_ui, 0)
        self.trigger = Clock.create_trigger(self.crop, 1)
        
    '''def init_ui(self, dt):
        print("----- RAIN 'init_ui'!!! ------")
        with self.ids.qr.ids.qrimage.canvas:
            # Bind cropping function to image texture updates
            Callback(texture=self.crop)'''

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
        '''
        Adds new member to spreadsheet
        '''
        
        '''self.export_to_png, self.export_as_image'''
        
        # Add to spreadsheet
        creds = self.app.get_creds()
        if not creds.valid:
            creds.refresh(Request())
        print("creds.valid =", creds.valid)
        if creds.expired:
            try:
                self.app.sheet = get_spread()
            except:
                self.app.spread_unloaded()
            
        print("creds.valid =", creds.valid)
        self.app.sheet.append_row([first_name.strip(),last_name.strip(), 'Beginner', 0, 'No', email, phone])
        button.disabled = True
        self.ids['home_button'].disabled = False
        self.ids['again_button'].disabled = False
        
        # Create QR Code
        self.ids['qr'].data = "{},{},{}".format(self.app.club_striped,first_name,last_name)
        self.trigger()
        
    def crop(self, *args):
        # Get and crop out QRcode from screenshot of current page
        texture = self.ids.qrBox.export_as_image("test").texture
        new_img = np.frombuffer(texture.pixels, np.uint8)
        height, width = texture.height, texture.width
        img = new_img.reshape(height, width, 4)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        #print("super: ", dir(super(AddMember, self)))
        #print()
        print("self.ids.qr.ids.qrimage: ", dir(self.ids.qr.ids.qrimage))
        print()
        #print()
        #print("self.children:", self.children)
        
        '''
        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        '''
        
        creds = self.app.get_creds()
        #d_creds = creds.with_subject('bdezius@gmail.com')
        print("creds.service_account_email =", creds.service_account_email)
        
        cv2.imwrite('./qrcode.png', img)
        '''message = create_email(
                    creds.service_account_email, 
                    self.ids['mem_email'].text, 
                    self.app.store.get("Settings")["Club name"] + " Membership QRcode",
                    "Welcome!!",
                    "./qrcode.png")'''
                    
        creds.refresh(Request())
        print("creds.valid =", creds.valid)
        service = build(u'drive', u'v3', credentials=creds)
        #send_email(service, 'me', message)
        
        # Upload QRcode
        webUrlLink = self.upload(service, './qrcode.png')
        
        # Email message with link
        import urllib.parse
        subject = "Welcome!!"
        body = \
"""Thanks for joining! We're happy to have you.
Here's the GoogleDrive link to your personal QRcode below (copy and paste into browswer if needed):

{}

Make sure to save/screenshot the QRcode for signing in. Can't wait to see you!!

-See you next class!
Pulso Caribe at UCF

""".format(webUrlLink)
        webbrowser.open("mailto:?to=" + self.ids['mem_email'].text + "&subject=" + urllib.parse.quote(subject) + "&body=" + urllib.parse.quote(body), new=1)
        
    def upload(self, drive_service, file_path):
        '''Uploads file to drive and returns weblink
        '''
    
        file_metadata = {
            'name': '{}_{}.png'.format(self.ids['first_name'].text, self.ids['last_name'].text),
            'parents': [self.app.folderID],
        }
        media = MediaFileUpload(file_path,
                                mimetype='image/png')
        file = drive_service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id, webViewLink').execute()
        print('File ID: %s' % file.get('id'))
        file_id = file.get('id')
        
        # Share with main account
        batch = drive_service.new_batch_http_request()
        user_permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': self.app.store.get("Settings")["Primary contact"]
        }
        batch.add(drive_service.permissions().create(
            fileId=file_id,
            body=user_permission,
            fields='id',
        ))
        batch.execute()
        
        return file.get('webViewLink')
    
    def open_online(self):
        sheet = self.app.get_spread()
        url_id = sheet.url.split('/')[-1]
        webbrowser.open("https://docs.google.com/spreadsheets/d/{}".format(url_id), new=2)
        
    def confirm(self, button):
    
        if len(self.ids['first_name'].text) < 1 or  len(self.ids['last_name'].text) < 1:
            self.app.updates = "Error: Enter both First and Last name."
            self.app.popup.open()
            return
        
        if re.search(regex, self.ids['mem_email'].text):
            button.disabled = True
            self.ids['confirm_button'].disabled = False
        else:
            self.app.updates = "Error: Confirm email is correct."
            self.app.popup.open()
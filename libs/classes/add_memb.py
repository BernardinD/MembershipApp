from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen

class AddMember(Screen):
   
	def __init__(self, **kwargs):
		super(AddMember, self).__init__(**kwargs)
		self.app = MDApp.get_running_app()

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
        
        # Add to spreadsheet
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
        
		# Create QR Code
		self.ids['qr'].data = "{},{},{}".format(self.app.club_striped,first_name,last_name)

	def confirm(self, button):
		button.disabled = True
		self.ids['confirm_button'].disabled = False
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen

class Scan(Screen):
	
	def __init__(self, **kwargs):
		#self.manager = manager
		super(Scan, self).__init__(**kwargs)
		self.screen = False
		self.app = MDApp.get_running_app()
		
	def scanned(self):
		"""
		A function executed when a qrcode is detected.
		"""
		# The on_symbols event is also fired when list gets empty, then it would raise an IndexError
		if self.ids.zbarcam.symbols and self.screen:
			symbol = self.ids.zbarcam.symbols[0]
			data = symbol.data.decode('utf8')
			print(data)
			# If unique identifier is in the QRCode, continue process
			if self.app.club_striped in data:
				temp = data.split(',')
				if len(temp) < 2:
					return
				qrfound_screen = self.app.changeScreen('verify_screen')
					
				if qrfound_screen:
					# Clearing property every single time because callback
                    #will not be called if new and old data are the same
					qrfound_screen.data_property = ""
					qrfound_screen.data_property = data
			
	def on_enter(self):
		#self.ids['zbarcam'].start()
		self.screen = True
	def on_pre_leave(self):
		#self.ids['zbarcam'].stop()
		self.screen = False
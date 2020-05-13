from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
class Home(Screen):
	def __init__(self, **kwargs):
		#self.manager = manager
		super(Home, self).__init__(**kwargs)
		self.app = MDApp.get_running_app()
		
	def show_add(self):
		self.app.changeScreen('add_screen')
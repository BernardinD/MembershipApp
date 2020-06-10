from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, BooleanProperty, NumericProperty

class Verify(Screen):
	data_property = StringProperty()

	prompt_property = StringProperty()
	col_property = NumericProperty()
	flag_property = BooleanProperty() # Defaults to True
	
	def __init__(self, **kwargs):
		#self.manager = manager
		#self.symbol = ''
		self.row = None
		super(Verify, self).__init__(**kwargs)
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
					levels_obj.background_color = (self.app.levels[level]) if ('No' in self.app.sheet.cell(row, 5).value) or self.col_property == 3  else (0,0,0,1)
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
		levels = self.app.levels
		curr_level = list(levels.keys()).index(self.ids['level'].text)
		return list(levels.keys())[curr_level+1] if curr_level+1 < len( (levels.keys()) ) else list(levels.keys())[curr_level]
		
	def cancel(self):
		self.app.on_back()
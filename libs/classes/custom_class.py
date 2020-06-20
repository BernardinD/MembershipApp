from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivymd.uix.label import Label
import os
Builder.load_file(os.path.join(
            os.environ["PULSO_APP_ROOT"], "libs", "kv",
            "subclass.kv"))

class CustomClass(BoxLayout):
	def __init__(self, **kwargs):
		super(CustomClass, self).__init__(**kwargs)
		
class SubClass(CustomClass):
	def __init__(self, **kwargs):
		super(SubClass, self).__init__(**kwargs)
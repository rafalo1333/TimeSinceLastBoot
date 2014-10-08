# -*- coding: utf-8 -*-

# Kivy imports

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform
from kivy.properties import NumericProperty, StringProperty
from kivy.event import EventDispatcher
from kivy.uix.image import Image
from kivy.base import EventLoop

# jnius imports && autoclasses

if platform=="android":
	from jnius import autoclass
	SystemClock=autoclass("android.os.SystemClock")
	PythonActivity=autoclass("org.renpy.android.PythonActivity")

kivy.require("1.8.0")
		
class ClockController(EventDispatcher):

	time_mls=NumericProperty()
	TIME_SINCE_BOOT=StringProperty("")
	
	def __init__(self):
		Clock.schedule_interval(self.count_uptime, 1)
		
	def count_uptime(self, *args):
		if platform=="android":
			self.time_mls=SystemClock.elapsedRealtime()
			self.seconds=(self.time_mls%60000)/1000
			self.minutes=(self.time_mls%3600000)/60000
			self.hours=self.time_mls/3600000
			self.TIME_SINCE_BOOT="Time since last boot: "+str(self.hours)+" hours, "+str(self.minutes)+" minutes, "+str(self.seconds)+" seconds."
		
class MainView(BoxLayout):
	pass
	
class AboutView(BoxLayout):
	pass
	
class BottomBar(Button):
	pass
	
class TopBar(BoxLayout):
	pass
		
class MainWindow(BoxLayout):

	def __init__(self, **kwargs):
		super(MainWindow, self).__init__(**kwargs)
		self.mainview=MainView()
		self.aboutview=AboutView()
	
	def show_about_view(self):
		self.clear_widgets()
		self.add_widget(self.aboutview)
		
	def show_main_view(self):
		self.clear_widgets()
		self.add_widget(self.mainview)
	
class TimeSinceLastBootApp(App):

	def __init__(self, **kwargs):
		super(TimeSinceLastBootApp, self).__init__(**kwargs)
		self.clockController=ClockController()
		
	def hook_keyboard(self, window, key, *largs):
		if key in [27, 1001]:
			if not self.adsController.show_ads():
				self.close_app()
			return True
		return False
		
	def open_settings_screen(self):
		pass
		
	def on_pause(self):
		return True
		
	def on_start(self):
		use_kivy_settings=False
		EventLoop.window.bind(on_keyboard=self.hook_keyboard)
	
	def close_app(self):
		self.stop()
		
if __name__=="__main__":
	TimeSinceLastBootApp().run()

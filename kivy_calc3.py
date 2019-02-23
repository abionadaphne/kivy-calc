from kivy.app import App
from kivy.uix.boxlayout	import BoxLayout 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.config import Config

Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '300')
Config.set('graphics', 'resizable', '0')

SaveInput=""

class CalculatorApp(App):
	def build(self):
		root=BoxLayout(orientation='vertical', padding=1)
		self.result=TextInput(readonly=True, font_size=24, size_hint=[1, .75], background_color=[3,2,1,2])
		root.add_widget(self.result)

		allButtons=GridLayout(cols=5)
		allButtons_list=['7','8','9','+','<','4','5','6','-','(','1','2','3','*',')','0','.','=','/','%']
		
		for button in allButtons_list:
			allButtons.add_widget(Button(text=button,on_press=self.calculate))
		root.add_widget(allButtons)

		return root

	def calculate(self, symbol):
		global SaveInput
		if symbol.text=='<':
			SaveInput=self.result.text=""
		elif symbol.text!='=':
			self.result.text+=symbol.text
			SaveInput+=symbol.text
		else:
			try:
				SaveInput=self.result.text=str(eval(SaveInput))
			except:
				SaveInput=self.result.text=""

if __name__=='__main__':
	CalculatorApp().run()

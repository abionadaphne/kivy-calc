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
#----------------------------------------------------
def isOp(c):
    if c != "": return (c in "+-*/")
    else: return False

def pri(c): # operator priority
    if c in "+-": return 0
    if c in "*/": return 1
    
def isNum(c):
    if c != "": return (c in "0123456789.")
    else: return False

def calc(op, num1, num2):
    if op == "+": return str(float(num1) + float(num2))
    if op == "-": return str(float(num1) - float(num2))
    if op == "*": return str(float(num1) * float(num2))
    if op == "/": return str(float(num1) / float(num2))

def Infix(expr):
    expr = list(expr)
    stackChr = list() # character stack
    stackNum = list() # number stack
    num = ""
    while len(expr) > 0:
        c = expr.pop(0)
        if len(expr) > 0: d = expr[0]
        else: d = ""
        if isNum(c):
            num += c
            if not isNum(d):
                stackNum.append(num)
                num = ""
        elif isOp(c):
            while True:
                if len(stackChr) > 0: top = stackChr[-1]
                else: top = ""
                if isOp(top):
                    if not pri(c) > pri(top):
                        num2 = stackNum.pop()
                        op = stackChr.pop()
                        num1 = stackNum.pop()
                        stackNum.append(calc(op, num1, num2))
                    else:
                        stackChr.append(c)
                        break
                else:
                    stackChr.append(c)
                    break
        elif c == "(":
            stackChr.append(c)
        elif c == ")":
            while len(stackChr) > 0:
                c = stackChr.pop()
                if c == "(":
                    break
                elif isOp(c):
                    num2 = stackNum.pop()
                    num1 = stackNum.pop()
                    stackNum.append(calc(c, num1, num2))

    while len(stackChr) > 0:
        c = stackChr.pop()
        if c == "(":
            break
        elif isOp(c):
            num2 = stackNum.pop()
            num1 = stackNum.pop()
            stackNum.append(calc(c, num1, num2))

    return stackNum.pop()

	
	
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
				SaveInput=self.result.text=str(Infix(SaveInput))
			except:
				SaveInput=self.result.text=""

if __name__=='__main__':
	CalculatorApp().run()
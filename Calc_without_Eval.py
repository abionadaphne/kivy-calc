from kivy.app import App
from kivy.uix.boxlayout	import BoxLayout 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.config import Config
import re
import time

Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '300')
Config.set('graphics', 'resizable', '0')

SaveInput=""
DIGITS = '0123456789'
OPS = '+-*/^'
OP_FUNCS = {
    '+':lambda x, y:x + y,
    '-':lambda x, y:x - y,
    '*':lambda x, y:x * y,
    '/':lambda x, y:x / y,
    '^':lambda x, y:x ** y,
}
ORDER_OF_OPERATIONS = [
    ['^'],
    ['*', '/'],
    ['+', '-'],
]
VALID_PAIRS = [
    ('NUM', 'OP'),
    ('OP', 'NUM'),
    ('OP', 'OPAREN'),
    ('CPAREN', 'OP'),
    ('OPAREN', 'NUM'),
    ('NUM', 'CPAREN'),
    ('OPAREN', 'OPAREN'),
    ('CPAREN', 'CPAREN'),
]
NUM_MATCH = re.compile(
'(?:[1-9][0-9]*|0)'
'(?:[.][0-9]+)?'
)


#---------------------------
class Token():  #This is not really useful but tuples could be less clear
    def __init__(self, type_, info=None):
        self.type = type_
        self.info = info
#    def __str__(self):
#        return '{}:{}'.format(self.type, self.info)
PLACEHOLDER = Token('PLACEHOLDER')
def tokenize(expr):
    tokens = []
    index = 0
    while index<len(expr):
        curr_and_after = expr[index:]
        is_num = NUM_MATCH.match(curr_and_after)
        if expr[index] in OPS:
            tokens.append(Token('OP', expr[index]))
        elif is_num:  
            num = is_num.group(0)
            tokens.append(Token('NUM', float(num)))
            length = len(num)
            index += length-1
        elif expr[index] == '(':
            tokens.append(Token('OPAREN'))
        elif expr[index] == ')':
            tokens.append(Token('CPAREN'))
        elif expr[index] == ' ':
          pass
        else:
          raise SyntaxError('Invalid character')
        index += 1
    return tokens
def is_valid(tokens):
    if tokens == []:
        return False

    #This sections tests if parentheses are correctly nested
    nesting = 0
    for token in tokens:
        if token.type == 'OPAREN':
            nesting += 1
        elif token.type == 'CPAREN':
            nesting -= 1
        if nesting<0:
            return False
    if nesting != 0:
        return False

    for index, _ in enumerate(tokens[:-1]):
        #[:-1] because otherwise next wont exist on last token
        curr, next_ = tokens[index], tokens[index+1]
        curr_kind, next_kind = curr.type, next_.type
        possible_valid_pairs = []
        for valid_pair in VALID_PAIRS:
            possible_valid_pairs.append((curr_kind, next_kind) == valid_pair)
            #Test if it's equal to a valid pair
        if not any(possible_valid_pairs):
            return False

    return True

def to_nested(tokens):
    assert(is_valid(tokens))
    out = []
    index = 0
    while index<len(tokens):
        if tokens[index].type == 'OPAREN':
            nesting = 1
            in_parens = []
            while nesting:
                index += 1
                if tokens[index].type == 'OPAREN':
                    nesting += 1
                elif tokens[index].type == 'CPAREN':
                    nesting -= 1
                in_parens.append(tokens[index])
            in_parens=in_parens[:-1]  #Remove final closing paren
            out.append(in_parens)
        else:
            out.append(tokens[index])
        index += 1
    return out
def has_op(tokens, op):
    return any([token.type == 'OP' and token.info == op for token in tokens])
def eval_tokens(tokens):
    newTokens = []
    for item in tokens:
        if type(item) == list:
          #Parenthesised expressions are lists of tokens
            newTokens.append(Token('NUM', eval_tokens(item)))
        else:
            newTokens.append(item)
    tokens = newTokens
    for ops_to_evaluate in ORDER_OF_OPERATIONS:
        newTokens = []
        while any([has_op(tokens, op) for op in ops_to_evaluate]):
          #While any of the ops exists in the expression
            for index, token in enumerate(tokens):
                if token.type == 'OP' and token.info in ops_to_evaluate:
                    where = index
                    func = OP_FUNCS[token.info] #Get a function for the operation
                    break
            fst, snd = tokens[where-1].info, tokens[where+1].info
            before, after = tokens[:where-1], tokens[where+2:]
            result = Token('NUM', func(fst, snd))
            tokens = before+[result]+after  #Recombine everything
    assert(len(tokens) == 1)  #Should always be true but for debugging it's useful
    assert(tokens[0].type == 'NUM')
    return tokens[0].info
def eval_expr(expr):
    tokens = tokenize(expr)
    nested = to_nested(tokens)
    return eval_tokens(nested)
	
#--------------------------------------CALCULATOR---------------------------------

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
				SaveInput=self.result.text=str(eval_expr(SaveInput))
			except:
				SaveInput=self.result.text=""

	
#---------------MAIN FUNCTION-------------------
if __name__=='__main__':
	CalculatorApp().run()
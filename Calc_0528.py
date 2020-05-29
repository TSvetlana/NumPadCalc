# -*- coding: utf-8 -*-
"""
Created on Wed May 13 16:29:42 2020

@author: Sveta
"""


#from tkinter import Tk, Entry, END, Text #Button
from tkinter import *
from tkinter import ttk
import math
from decimal import Decimal
import os # for MacOS only
from system_hotkey import SystemHotkey # not supported by MacOS => to be commented out for MacOS
#import time


class Calc:
	def getandreplace(self):  # replace x, + and % to symbols that can be used in calculations
# 		# we wont re write this to the text box until we are done with calculations

		self.txt = self.e.get() # Get value from text box and assign it to the global txt var
		self.txt = self.txt.replace('^', '**')
		self.txt = self.txt.replace('÷', '/')
		self.txt = self.txt.replace('x', '*')
		

	def evalorresult(self):
		self.txt = self.e.get()
		self.idx = self.txt.find('=')
		if self.idx > 0:
			self.txt = self.txt[self.idx+2: ]
			
			if any(x in self.txt for x in '+-/*'):# and not float(self.txt) or not int(self.txt): #or not math.fabs(float(self.txt)).isdigit()
				self.e.delete(0, END)
				self.e.insert(0,self.txt)
				self.evaluation('eq')
			else: #if self.txt[0]=='-' and float(self.txt) or int(self.txt):
				self.e.delete(0, END)
				self.e.insert(0,self.txt)
		else:
			self.evaluation('eq')

	def evalorresultspec(self):
		#self.txt = self.e.get()
		self.idx = self.txt.find('=')
		if self.idx > 0:
 			self.txt = self.txt[self.idx+2: ]
 			self.e.delete(0, END)
 			self.e.insert(0,self.txt)
		elif any(x in self.txt for x in '/*-+'):
			self.txt = self.floatorint(float(eval(str(self.txt))))


	def getpercent(self):
		#self.txt = self.e.get()
		index=0
		if any(x in self.txt for x in '/*'):
			if self.txt.find('*')>0:
				index=self.txt.find('*')
			else:
				index=self.txt.find('/')

			self.txt=self.txt.replace('%', '/100)')
			self.txt=self.txt[0:index+1] + '(' +self.txt[index+1:]
			return self.floatorint(eval(self.txt))
		else:
			if self.txt.find('+')>=0 :
				index=self.txt.find('+')
			elif self.txt.find('-')>=0:
				index=self.txt.find('-')
			substr1=self.txt[ :index]
			substr2=self.txt[(index+1):-1]
			substr3=float(substr1)*float(substr2)/100
			return self.floatorint(eval(self.txt[:index+1]+str(substr3)))

	def evaluation(self, specfunc):  # Evaluate the items in the text box for calculation specfunc = eq, sqroot or square
		self.getandreplace()
		is_digit=self.txt.isdigit()
		if self.txt.endswith('%'):
			try: 
				self.txt = self.getpercent()
			except:
				self.displayinvalid()
			else:
				self.refreshtext(self.txt)
				self.e.focus_set()
		elif any([specfunc == 'sqroot', specfunc == 'square', specfunc == 'LOG10', specfunc== '10^x', specfunc == '1/X',
				specfunc == 'sin', specfunc == 'cos', specfunc == 'tan', specfunc == 'PI', specfunc == 'lnX', specfunc == 'exp']):  #specfunc == '1/X',
			try: # Square Root and square are special
				
				self.evalorresultspec()  #evalorresultspec
				self.txt = self.evalspecialfunctions(specfunc)
			except:
				self.displayinvalid()
			else:
				if specfunc == 'PI':
					if len(self.e.get())>0 and self.e.get()[-1].isdigit():
						self.e.delete(0,'end')
						self.e.insert(END,str(self.txt))
					else:
						self.e.insert(END,str(self.txt))
					#self.refreshtextpi(self.txt)
				else:
					self.refreshinsertedtext(specfunc,is_digit)
					self.refreshtext(self.txt)
				self.e.focus_set()
		elif any(x in self.txt for x in '/*-+') and not any(map(str.isalpha, self.txt)):
			try:
				self.txt = self.floatorint(float(eval(str(self.txt))))  # evaluate the expression using the eval function float('{:.13f}'.format(eval(str(self.txt))))

			except ZeroDivisionError:
				self.e.delete(0, 'end')
				self.e.insert(0, 'Division by Zero!')
				self.e.focus_set()
			except:
				self.displayinvalid()
			else:
				self.refreshtext(self.txt)
				self.e.focus_set()
				
		elif not any(x in self.txt for x in '/*-+') and any(map(str.isalpha, self.txt)):
			try:
				self.txt='math.'+self.txt
				self.txt = self.floatorint(float(eval(str(self.txt))))  # evaluate the expression using the eval function float('{:.13f}'.format(eval(str(self.txt))))
			except:
				self.displayinvalid()
			else:
				self.refreshtext(self.txt)
				self.e.focus_set()
		elif any(x in self.txt for x in '/*-+') and any(map(str.isalpha, self.txt)):
			self.txt=self.txt.replace(" ","")
			count=0
			list=[]
			if self.txt[0].isalpha():
				list.append(0)
			for x in self.txt:
				if x.isalpha():
					if self.txt[count-1] in '/+*-':
						list.append(count)
				count+=1
			idx=0
			for x in list:

				self.txt= self.txt[0:x+idx] + 'math.'+ self.txt[x+idx:]
				idx+=5
			print(self.txt)
			try:
				self.txt = self.floatorint(float(eval(str(self.txt))))  # evaluate the expression using the eval function float('{:.13f}'.format(eval(str(self.txt))))
			
			except:
				self.displayinvalid()
			else:
				self.refreshtext(self.txt)
				self.e.focus_set()

	def floatorint(self, equation):
		if int(equation)==float(equation) and len(str(equation))<10:
			print(len(str(equation)))
			return int(equation)
		elif int(equation)==float(equation) and len(str(equation))>9:
			print(len(str(equation)))
			return "{:.7e}".format(Decimal(equation))
		else:
			print(len(str(equation)))
			return float('%.13g' % equation)

	def refreshinsertedtext(self,specfunc, is_digit):
		if specfunc == 'sqroot':
			self.e.insert(0,'sqrt(')
			self.e.insert('end',')')
		elif specfunc == 'LOG10':
			self.e.insert(0,'log10(')
			self.e.insert('end',')')
		elif specfunc == 'square':
			if not is_digit:
				self.e.insert(0,'(')
				self.e.insert('end',')²')
			else:
				self.e.insert('end','²')
		elif specfunc == '10^x':
			if not is_digit:
				self.e.insert(0,'10^(')
				self.e.insert('end',')')
			else:
				self.e.insert(0,'10^')
		elif specfunc == 'cos':
			self.e.insert(0,'cos(')
			self.e.insert('end',')')
		elif specfunc == 'sin':
			self.e.insert(0,'sin(')
			self.e.insert('end',')')
		elif specfunc == 'tan':
			self.e.insert(0,'tan(')
			self.e.insert('end',')')
		elif specfunc == '1/X':
			if not is_digit:
				self.e.insert(0,'1/(')
				self.e.insert('end',')')
			else:
				self.e.insert(0,'1/')
		elif specfunc == 'lnX':
			self.e.insert(0,'ln(')
			self.e.insert('end',')')
		elif specfunc == 'exp':
			self.e.insert(0,'exp(')
			self.e.insert('end',')')

	def changeinseredtext(self):
		cursor_pos = self.e.index('insert')
		self.txt= self.e.get()
		if self.txt.find('=')> 0:
			if cursor_pos < self.txt.find('=') :
				self.e.delete(self.txt.find('=')-1,'end')
			elif cursor_pos > self.txt.find('='):
				self.e.delete(self.txt.find('='),'end')

	def displayinvalid(self):
		self.e.delete(0, 'end')
		self.e.insert(0, 'Invalid Input!')
		self.e.focus_set()

	def refreshtext(self,equation):  # Delete current contents of textbox and replace with our completed evaluatioin
		self.e.insert('end'," = " + str(self.txt))
		self.lb.insert('end', str(self.e.get()))
		self.lb.see('end')
		self.e.xview_moveto(0)

	def evalspecialfunctions(self, specfunc):  # Calculate square root and square if specfunc is sqroot or square
		if specfunc == 'sqroot':
			return self.floatorint(math.sqrt(float(self.txt)))
		elif specfunc == 'square':
			return self.floatorint(math.pow(float(self.txt), 2))
		elif specfunc == 'LOG10':
			return self.floatorint(math.log10(float(self.txt)))
		elif specfunc== '10^x':
			return self.floatorint(math.pow(10, float(self.txt)))
		elif specfunc== 'cos':
			if self.r_var.get()==0:
				answer= math.cos(math.radians(float(self.txt)))
			else:
				answer= math.cos(float(self.txt))
			return self.floatorint(answer)
		elif specfunc== 'sin':
			if self.r_var.get()==0:
				answer= math.sin(math.radians(float(self.txt)))
			else:
				answer= math.sin(float(self.txt))
			return self.floatorint(answer)
		elif specfunc== 'tan':
			if self.r_var.get()==0:
				answer= math.tan(math.radians(float(self.txt)))
			else:
				answer= math.tan(float(self.txt))
			return self.floatorint(answer)
		elif specfunc== '1/X':
			return self.floatorint(float(eval(str(1/float(self.txt)))))
		elif specfunc== 'exp':
			return self.floatorint(math.exp(float(self.txt)))
		elif specfunc== 'lnX':
			return self.floatorint(math.log(float(self.txt)))
		elif specfunc== 'PI':
			return math.pi

	def keyaction(self, event=None):  # Key pressed on keyboard which defines event
		if event.char == '\x1b': #escape
			self.lb.delete(0,END)
		elif event.char == '\x08' or event.keysym=='BackSpace': #backspace
			self.changeinseredtext()
		elif event.keysym=='Delete':
			self.e.delete(0, END)
		elif event.char == '\r' or event.keysym=='KP_Enter': #return    event.keysym=='KP_Enter' - numpad Enter, MacOS
			self.evalorresult()
		elif event.char == "\x0c": #log10; '<Control-l>'
			self.evaluation('LOG10')
		elif event.char=="\x04" or event.keysym=='F13':#Control-D, F13 or Num_Lock
			root.destroy() # close Calculator with Control-D

	def iconifyordeiconify(self):
		if root.wm_state()=='withdrawn':
			root.deiconify()
			self.e.focus_set()
		else:
			root.withdraw()

	def listboxclick(self, event):
		self.e.delete(0, 'end')
		self.e.insert(0, str(self.lb.get('active')))#self.lb.curselection()
		self.e.focus_set()
		root.clipboard_clear()
		self.selected = self.lb.get('anchor')
		root.clipboard_append(self.selected)

	def onselect(self, event):
		self.txt = self.e.get()
		
		if self.txt.find('=')<0:
			if any(x in self.txt for x in '/*-+'):
				self.txt = self.floatorint(float(eval(str(self.txt))))
				self.e.insert('end'," = " + str(self.txt))
		else:
			if any(x in self.txt for x in '/*-+'):
				self.e.delete(0,self.txt.find('=')+2) #self.txt.find('=')-1,'end'
				self.txt= self.txt[self.txt.find('=')+1:]
				
			else:
				self.e.delete(self.txt.find('=')-1,'end') #self.txt.find('=')-1,'end'
				self.txt= self.txt[0:self.txt.find('=')-1]
			
		if self.cb.get() =='Hex':
			self.txt= hex(int(self.txt))
		elif self.cb.get() =='Binary':
			self.txt= bin(int(self.txt))
		elif self.cb.get() =='Octal':
			self.txt= oct(int(self.txt))
		self.refreshtext(self.txt)

	def about(self):
		self.about_window = Toplevel(root) #Tk()
		self.about_window.title("About Calculator TRETYAKOV")
		self.about_window.geometry()
		self.about_window.config(bg='gray96', padx=2, pady=4)
		self.about_window.lift(root)
		#root1.call('wm', 'attributes', '.', '-topmost', '1')
		text = Text(self.about_window, wrap=WORD, width=35,height=20, bg="gray96", relief='flat', font=('Arial', 12))
		quote="""Esc	- clear history
Delete	- clear entry 
Pause / NumLock	- hide / show

Double click on history line brings expression back to expression field

For mathematical functions not available from GUI buttons simply try writing them directly in expression field, if Python supports them, they will work. Example factorial(25)"""
		text.insert(END, quote)
		text.grid(sticky='nw', padx=3, pady=4)
		self.about_window.focus_set()
		self.about_window.grab_set() 

	def degreesorradians(self):
		self.txt=self.e.get()
		firstchar=self.txt[0]
		myList = ['sin', 'cos','tan']
		if any(x in self.txt for x in myList):
			self.txt=self.txt[4:self.txt.find(')')]
			self.e.delete(0, END)
			self.e.insert(0,self.txt)
			if firstchar=='c':
				self.evaluation('cos')
			elif firstchar=='s':
				self.evaluation('sin')
			elif firstchar=='t':
				self.evaluation('tan')

	def __init__(self, master):# Constructor method
		self.txt = '0'  # Global var to work with text box contents
		master.title('Calculator TRETYAKOV')
		w = master.winfo_screenwidth() # width of display
		h = master.winfo_screenheight() # hight of display
		w = w//2 # center of display
		h = h//2 # center of display
		w = w - 300 # offset from center
		h = h - 200 # offset from center
		master.geometry('+{}+{}'.format(w, h))
		master.configure(bg='gray94', padx=2, pady=4)#lavender, azure2
		master.grid_columnconfigure(0, weight=1)
		master.grid_rowconfigure(0, weight=1)
		self.e = ttk.Entry(master, font=('Helvetica', 20, 'bold'))
		self.e.grid(sticky=EW,row=1, columnspan=5, padx=3, pady=3)
		self.e.focus_set()  # Sets focus on the text box text area   _set
		
		self.lb = Listbox(master, height=7, bg="gray94", fg='gray10', font=('Courier New', 12, 'bold'), relief='flat', selectmode='single', activestyle='none')#width=32,,Helvetica 
		self.lb.grid(sticky="nsew",row=0, columnspan=5, padx=3, pady=3)
		scroll_lb = ttk.Scrollbar( orient=VERTICAL, command=self.lb.yview)
		scroll_lb.grid(sticky='nse',column=4, row=0)
		self.lb.config(yscrollcommand=scroll_lb.set)
		self.lb.bind("<Double-Button-1>", self.listboxclick) #ListboxSelect, <Double-Button-1>
		
		self.r_var = IntVar()
		self.r_var.set(0)
		self.degrees = Radiobutton(text='Degrees', variable=self.r_var, command= self.degreesorradians, value=0)
		self.radians = Radiobutton(text='Radians', variable=self.r_var, command=self.degreesorradians, value=1)
		self.degrees.grid(sticky="w",row=3, column=0, padx=3, pady=3)
		self.radians.grid(sticky="w",row=4, column=0, padx=3, pady=3)

		self.cb = ttk.Combobox(master, width=9, values=("Decimal", "Hex", "Binary", "Octal"))
		self.cb.set("Decimal")
		self.cb.grid(sticky="w",row=5, column=0)
		self.cb.bind('<<ComboboxSelected>>', self.onselect)
		
		# Generating Buttons
		ttk.Button(master, text="√", command=lambda: self.evaluation('sqroot')).grid(row=3, column=1, padx=2, pady=2) #, width=10
		ttk.Button(master, text="x²", command=lambda: self.evaluation('square')).grid(row=3, column=2, padx=2, pady=2)
		ttk.Button(master, text="LOG10", command=lambda: self.evaluation('LOG10')).grid(row=3, column=3, padx=2, pady=2)
		ttk.Button(master, text="10ˣ", command=lambda: self.evaluation('10^x')).grid(row=3, column=4, padx=2, pady=2)
		ttk.Button(master, text="cos", command=lambda: self.evaluation('cos')).grid(row=4, column=1, padx=2, pady=2)
		ttk.Button(master, text="sin", command=lambda: self.evaluation('sin')).grid(row=4, column=2, padx=2, pady=2)
		ttk.Button(master, text="tan", command=lambda: self.evaluation('tan')).grid(row=4, column=3, padx=2, pady=2)
		ttk.Button(master, text="1/X", command=lambda: self.evaluation('1/X')).grid(row=4, column=4, padx=2, pady=2)
		ttk.Button(master, text="exp", command=lambda: self.evaluation('exp')).grid(row=5, column=1, padx=2, pady=2)
		ttk.Button(master, text="lnX", command=lambda: self.evaluation('lnX')).grid(row=5, column=2, padx=2, pady=2)
		ttk.Button(master, text="PI", command=lambda: self.evaluation('PI')).grid(row=5, column=3, padx=2, pady=2)
		ttk.Button(master, text="Help", command = self.about).grid(row=5, column=4, padx=2, pady=2)
		
		# bind key strokes
		self.e.bind('<Key>', lambda evt: self.keyaction(evt))
		
		hk = SystemHotkey()# not supported by MacOS => to be commented out for MacOS
		hk2 = SystemHotkey()# not supported by MacOS => to be commented out for MacOS
		hk.register(['kp_numlock'], overwrite=True, callback=lambda event: self.iconifyordeiconify())# not supported by MacOS => to be commented out for MacOS
		hk2.register(['pause'], overwrite=True, callback=lambda event: self.iconifyordeiconify())# not supported by MacOS => to be commented out for MacOS


# Main
root = Tk()
obj = Calc(root)  # object instantiated
root.call('wm', 'attributes', '.', '-topmost', '1')# sets calculator visible all the time (always on top)
os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')# brings Calculator in focus for Macos
#https://stackoverflow.com/questions/1892339/how-to-make-a-tkinter-window-jump-to-the-front

root.mainloop()

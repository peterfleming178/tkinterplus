import tkinter as tk

class ElementBox(tk.Label):
	def interactive(self,colour):
		bg = self.cget("bg")

		def enter(arg=None):
			self.config(bg=colour)
		def leave(arg=None):
			self.config(bg=bg)

		
		self.bind("<Enter>",enter)
		self.bind("<Leave>",leave)

def rgb(r,g,b):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return f'#{r:02x}{g:02x}{b:02x}'

class CodeEditor(Text):
	def __init__(self,master,draggable=False,sublimetheme=False,theme=None,**args):
		super().__init__(master=master,**args)
		self.theme = theme
		if self.theme != None:
			if self.theme == 'python':
				self.scheme_python()
				self.bind("<Key>",self.scheme_python)
		self.draggable = draggable
		if self.draggable == True:
			self.make_draggable()
		if sublimetheme == True:
			self.sublimetheme()

	def sublimetheme(self,arg=None):
		self.config(bg="#272923",fg="#f7f8f2",insertbackground="#f7f8f2")
		return "#272923","#f7f8f2"
	def clear(self):
		self.delete('1.0','end')
	def find(self,word='',background='red',foreground='white'): 
		s = word
		self.tag_remove('found', '1.0', END) 
		if s: 
			idx = '1.0'
			while True: 
				idx = self.search(s, idx, nocase=1,stopindex=END) 
				if not idx: break
				lastidx = '%s+%dc' % (idx, len(s)) 
				self.tag_add('found', idx, lastidx) 
				idx = lastidx  
			self.tag_config('found', background=background,foreground=foreground)
	def paste(self):
		self.insert(self.index(INSERT),self.clipboard_get())
	def colorscheme(self,colour,word):
		for s in word:
			if s: 
				idx = '1.0'
				while True: 
					idx = self.search(s, idx, nocase=1,stopindex=END) 
					if not idx: break
					lastidx = '%s+%dc' % (idx, len(s)) 
					self.tag_add(colour, idx, lastidx) 
					idx = lastidx 
				self.tag_config(colour, foreground=colour)

	def curly(self,arg=None):
		position = self.index(INSERT)
		self.insert(position,"()")
		self.cursor_set_back()
		return 'break'

	def insert_tabs(self,arg=None):
		code_given = str(self.get(SEL_FIRST,SEL_LAST))
		code_given = code_given.splitlines()
		code_formatted = []
		for lines in code_given:
			code_formatted.append((" "*4)+lines)
		x,y = SEL_FIRST,SEL_LAST
		self.delete(x,y)
		code_formatted = '\n'.join(code_formatted)
		position = self.index(INSERT)
		self.insert(position,code_formatted)

	def remove_tabs(self,arg=None):
		code_given = str(self.get(SEL_FIRST,SEL_LAST))
		code_given = code_given.splitlines()
		code_formatted = []
		for lines in code_given:
			code_formatted.append(lines[4:])
		x,y = SEL_FIRST,SEL_LAST
		self.delete(x,y)
		code_formatted = '\n'.join(code_formatted)
		position = self.index(INSERT)
		self.insert(position,code_formatted)
		return 'break'

	def tab(self,arg=None):
		try: self.insert_tabs()
		except: pass
		self.insert(self.index(INSERT)," "*4)
		return 'break'

	def quotation1(self,arg=None):
		self.insert(self.index(INSERT),"''")
		self.cursor_set_back()
		return 'break'

	def cursor_set_back(self,arg=None):
		position = self.index(INSERT)
		position = position.split(".")
		position = [position[0],str(int(position[1])-1)]
		position = '.'.join(position)
		self.mark_set("insert", f"{position}")

	def quotation2(self,arg=None):
		self.insert(self.index(INSERT),'""')
		self.cursor_set_back()
		return 'break'

	def brackets(self,arg=None):
		self.insert(self.index(INSERT),'[]')
		self.cursor_set_back()
		return 'break'

	def curlybraces(self,arg=None):
		self.insert(self.index(INSERT),'{}')
		self.cursor_set_back()
		return 'break'

	def remove_line(self,arg=None):
		position = self.index(INSERT)
		position2 = position.split(".")
		position1 = float(position2[0]+".0")
		self.delete(str(position1),str(position))


	def scheme_python(self,arg=None):
		yellow =  ['"',"'",'""',"''"]

		purple =  ['True','False','1','2','3','4','5','6','7','8','9','0']

		cyan =  ['len','def ',' int',' str',
				' float',' bool',' sum','append',
				'print','zip','class']

		red =  ['if ','else ','while ','elif ','for ',' in ',
			  ' = ',' + ',' / ',' * ','import ','from ',' as ',
			  'global ',' not ','break',' % ','=!','+=','-']

		green = []

		keys = [[yellow,"#e8db61"],[purple,"#b57aff"],
				[cyan,"#23daf2"],[red,"#ff0070"],[green,"#92e500"]]

		for key in keys:
			self.colorscheme(word=key[0],colour=key[1])

	def keyboard(self,arg=None,linebar=None):
		self.bind("(",self.curly)
		self.bind("<Tab>",self.tab)
		self.bind("<Shift-Tab>",self.remove_tabs)
		if platform == "darwin":
			self.bind("<Command-BackSpace>",self.remove_line)
			self.bind("<Command-c>",self.copy)
		if linebar != None:
			self.bind("<Return>",linebar.run)
		self.bind("'",self.quotation1)
		self.bind('"',self.quotation2)
		self.bind("[",self.brackets)
		self.bind("{",self.curlybraces)

	def fit(self,master,onmotion=False):
		def on_drag_motion(self,master,event=None):
			width = master.winfo_width()
			height = master.winfo_height()
			self.config(width=width,height=height)
		on_drag_motion(self,master)
		if onmotion == True:
			master.bind("<Button-1>", lambda x: on_drag_motion(self=self,master=master))

	def getAll(self):
		return self.get('1.0','end-1c')

	def copy(self,args=None):
		self.clipboard_clear()
		try:
			text = str(self.get(SEL_FIRST,SEL_LAST))
		except:
			text = str(self.get('1.0','end'))
		self.clipboard_append(text)
		try:
			self.clipboard_update()
		except:
			pass


	def make_draggable(self):
		def drag_start(event):
			widget = self
			widget = event.widget
			self._drag_start_x = event.x
			self._drag_start_y = event.y

		def drag_motion(event):
			widget = self
			widget = event.widget
			x = self.winfo_x() - self._drag_start_x + event.x
			y = self.winfo_y() - self._drag_start_y + event.y
			self.place(x=x, y=y)
		self.bind("<Button-1>", drag_start)
		self.bind("<B1-Motion>", drag_motion)
	def lineview(self):
		return int(self.index('end-1c').split('.')[0])
	def defaultmenu(self):
		menu = Menu(self,tearoff=False)
		menu.add_command(label="Copy",command=self.copy)
		menu.add_command(label="Paste",command=self.paste)
		menu.add_command(label="Redo",command=self.edit_redo)
		menu.add_command(label="Undo",command=self.edit_undo)
		menu.add_command(label="Clear",command=self.clear)
		def popup(e):
			menu.tk_popup(e.x_root,e.y_root)
		self.bind("<Button-2>",popup)
		self.bind("<Button-3>",popup)

class Linebar(Text):
	def __init__(self,master,lineview,sublimetheme=False,**args):
		super().__init__(master=master,**args,width=3)
		self.lineview = lineview
		self.config(state=DISABLED)
		if sublimetheme == True:
			self.sublimetheme()
	def line(self,linenumber):
		self.linenumber = self.lineview.lineview
		def insert_():
			self.delete("1.0","end-1c")
			end = 0
			for i in range(1,int(self.linenumber())):
				self.insert(float(str(i)+".0"),str(i)+"	")
				end = i
			self.insert(float(str(end+1)+".0"),str(end+1)+"	")
		self.config(state='normal')
		insert_()
		self.config(state=DISABLED)

	def scroll(self,*args):
		self.yview(*args)
		self.lineview.yview(*args)		

	def sublimetheme(self,arg=None):
		self.config(bg="#272923",fg="#f7f8f2",insertbackground="#f7f8f2")
		return "#272923","#f7f8f2"

	def run(self,arg):
		s = self.line(linenumber=self.lineview)


#testing area

def test():
	#demo testing area


	window = Tk()



	scrollbar = Scrollbar(window,orient=VERTICAL)
	scrollbar.grid(row=0,column=2,sticky=N+S)

	s = CodeEditor(window,theme="python",sublimetheme=True,draggable=True,yscrollcommand=scrollbar.set,bg="white")
	s.grid(row=0,column=1)

	y = Linebar(window,bg="white",fg='black',yscrollcommand=scrollbar.set,lineview=s)
	y.grid(row=0,column=0)

	s.keyboard(linebar=y)
	s.sublimetheme()
	s.defaultmenu()

	scrollbar.config(command=y.scroll)
	Button(window,command=s.lineview).grid(row=1,column=1)
	window.mainloop()

if __name__ == "__main__":
	test()
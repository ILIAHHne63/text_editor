from tkinter import WORD, LEFT, Tk, Scrollbar, RIGHT, Y, Frame, Text, BOTH, Menu
from src.actions import Actions

class Editor:

    def WindowEditor(self):
        self.editor_window.title('TextEditor')
        self.editor_window.geometry('700x800')

    def FileMenuEditor(self):
        self.file_menu = Menu(self.main_menu)
        self.file_menu.add_command(label='Open', command=self.actions.OpenFile)
        self.file_menu.add_command(label='Find', command=self.actions.FindText)
        self.file_menu.add_command(label='Save', command=self.actions.SaveFile)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Delete')
        self.editor_window.config(menu=self.file_menu)

    def ViewMenuEditor(self):
        self.view_menu = Menu(self.main_menu)
        self.font_menu = Menu(self.view_menu)
        self.font_menu.add_command(label='Times New Roman', command=lambda: self.actions.ChangeFonts('TNR'))
        self.font_menu.add_command(label='Arial', command=lambda: self.actions.ChangeFonts('Arial'))
        self.font_menu.add_command(label='Courier New', command=lambda: self.actions.ChangeFonts('CN'))
        self.view_menu.add_cascade(label='Font', menu=self.font_menu)
        self.size_menu = Menu(self.view_menu)
        self.size_menu.add_command(label='10', command=lambda: self.actions.ChangeSize('10'))
        self.size_menu.add_command(label='20', command=lambda: self.actions.ChangeSize('20'))
        self.size_menu.add_command(label='30', command=lambda: self.actions.ChangeSize('30'))
        self.view_menu.add_cascade(label='Size', menu=self.size_menu)
        self.editor_window.config(menu=self.view_menu)

    def MenuEditor(self):
        self.main_menu = Menu(self.editor_window)

        self.FileMenuEditor()
        self.ViewMenuEditor()

        self.editor_window.config(menu=self.main_menu)
        self.main_menu.add_cascade(label='File', menu=self.file_menu)
        self.main_menu.add_cascade(label='View', menu=self.view_menu)

    def ScrollEditor(self):
        self.scroll = Scrollbar(self.text, command=self.text.yview)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.text.config(yscrollcommand=self.scroll.set)

    def TextEditor(self):
        self.widget = Frame(self.editor_window)
        self.widget.pack(fill=BOTH, expand=1)
        self.text = Text(self.widget,
                         fg='white',
                         bg='black',
                         padx=10,
                         pady=10,
                         wrap=WORD,
                         insertbackground='white',
                         spacing3=10)
        self.text.pack(fill=BOTH, side=LEFT, expand=1)

    def __init__(self):
        self.editor_window = Tk()
        self.TextEditor()

        self.actions = Actions(self.text)

        self.WindowEditor()
        self.MenuEditor()
        self.ScrollEditor()

        self.editor_window.bind('<Control-s>', self.actions.SaveFile)
        self.editor_window.bind('<Control-o>', self.actions.OpenFile)
        self.editor_window.bind('<Control-f>', self.actions.FindText)
        self.editor_window.bind('<Control-d>', self.actions.DeleteLine)
        self.editor_window.bind('<Control-w>', self.actions.DeleteWord)

        self.editor_window.mainloop()

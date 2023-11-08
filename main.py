import sys
from tkinter import *
from tkinter import filedialog, simpledialog, messagebox

import font

class Editor:
    def SaveFile(self, event=None):
        file_path = filedialog.asksaveasfilename(filetypes=(('Text Documents (*.txt)', '*.txt'), ('All Files', '*.*')))
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.text.get('1.0', END))

    def DeleteLine(self, event=None):
        current_line = self.text.index(INSERT).split('.')[0]
        start = f"{current_line}.0"
        end = f"{current_line}.end"
        self.text.delete(start, end)

    def DeleteWord(self, event=None):
        cursor_index = self.text.index(INSERT)
        end_index = self.text.search(r"\s", cursor_index, regexp=True)
        start_index = self.text.search(r"\s", cursor_index, backwards=True, regexp=True)
        if start_index == end_index:
            self.text.delete("1.0", end_index)
        if start_index == "" or end_index == "":
            return
        self.text.delete(start_index, end_index)


    def OpenFile(self, event=None):
        file_path = filedialog.askopenfilename(title='Выбор файла', filetypes=(('C++ files (*.cpp)', '*.cpp'), ('Python files (*.py)', '*.py'), ('Все файлы (*.*)', '*.*')))
        if file_path:
            self.text.delete('1.0', END)
            self.text.insert('1.0', open(file_path, encoding='utf-8').read())

    def FindText(self, event=None):
        search_query = simpledialog.askstring("Find", "Enter text to search:")
        if search_query:
            replace_query = simpledialog.askstring("Replace", "Enter text to replace:")
            start_pos = "1.0"
            while True:
                start_pos = self.text.search(search_query, start_pos, END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(search_query)}c"
                self.text.tag_add("search", start_pos, end_pos)
                if replace_query:
                    self.text.delete(start_pos, end_pos)
                    self.text.insert(start_pos, replace_query)
                elif self.text.tag_ranges("search"):
                    self.text.mark_set("insert", self.text.tag_ranges("search")[0])
                    self.text.see(self.text.tag_ranges("search")[0])
                    self.text.tag_config("search", background="grey")
                else:
                    messagebox.showinfo("Find", "Text not found.")
                start_pos = end_pos


    def ChangeFonts(self, font_to_change):
        self.text['font'] = font.fonts[font_to_change]['font']

    def WindowEditor(self):
        self.editor_window.title('TextEditor')
        self.editor_window.geometry('700x800')

    def FileMenuEditor(self):
        self.file_menu = Menu(self.main_menu)
        self.file_menu.add_command(label='Open', command=self.OpenFile)
        self.file_menu.add_command(label='Find', command=self.FindText)
        self.file_menu.add_command(label='Save', command=self.SaveFile)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Delete')
        self.editor_window.config(menu=self.file_menu)

    def ViewMenuEditor(self):
        self.view_menu = Menu(self.main_menu)
        self.font_menu = Menu(self.view_menu)
        self.font_menu.add_command(label='Times New Roman', command=lambda: self.ChangeFonts('TNR'))
        self.font_menu.add_command(label='Arial', command=lambda: self.ChangeFonts('Arial'))
        self.font_menu.add_command(label='Courier New', command=lambda: self.ChangeFonts('CN'))
        self.view_menu.add_cascade(label='Font', menu=self.font_menu)
        self.view_menu.add_command(label='Size')
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

        self.editor_window.bind('<Control-s>', self.SaveFile)
        self.editor_window.bind('<Control-o>', self.OpenFile)
        self.editor_window.bind('<Control-f>', self.FindText)
        self.editor_window.bind('<Control-d>', self.DeleteLine)
        self.editor_window.bind('<Control-w>', self.DeleteWord)

        self.WindowEditor()
        self.MenuEditor()
        self.TextEditor()
        self.ScrollEditor()

        self.editor_window.mainloop()

elem = Editor()

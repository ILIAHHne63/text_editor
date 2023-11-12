from tkinter import filedialog, simpledialog, messagebox, END, INSERT
from src import size, font


class Actions():

    def __init__(self, text):
        self.text = text

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
        file_path = filedialog.askopenfilename(title='Выбор файла', filetypes=(
        ('C++ files (*.cpp)', '*.cpp'), ('Python files (*.py)', '*.py'), ('Все файлы (*.*)', '*.*')))
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

    def ChangeSize(self, size_to_change):
        self.text['font'] = size.sizes[size_to_change]['size']

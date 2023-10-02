import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from INI_Mod.gui.syntax_highlighter import SyntaxHighlighter
from INI_Mod.utils.ini_parser import IniParser

class INIEditor:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.top_level = self.master.winfo_toplevel()
        self.top_level.title("INI File Editor")

        self.ini_parser = IniParser()
        self.syntax_highlighter = SyntaxHighlighter(self.frame)
        self.ini_text = self.syntax_highlighter.text_widget
        self.ini_text.config(bg='#2e2e2e', fg='white', insertbackground='white')  # Set dark background and white text

        self.create_widgets()
        self.create_menus()

    def create_widgets(self):
        self.status_label = tk.Label(self.frame, text="Welcome to INI-Mod", anchor=tk.W, bg='#333', fg='white')
        self.status_label.pack(fill=tk.BOTH)

        self.button_frame = tk.Frame(self.frame, bg='#333')  # Added a frame for buttons
        self.button_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.undo_button = tk.Button(self.button_frame, text="Undo", command=self.undo, bg='#444', fg='white')
        self.undo_button.pack(side=tk.LEFT, padx=5)

        self.redo_button = tk.Button(self.button_frame, text="Redo", command=self.redo, bg='#444', fg='white')
        self.redo_button.pack(side=tk.LEFT, padx=5)

        self.search_button = tk.Button(self.button_frame, text="Search", command=self.search_text, bg='#444', fg='white')
        self.search_button.pack(side=tk.LEFT, padx=5)

        self.replace_button = tk.Button(self.button_frame, text="Replace", command=self.replace_text, bg='#444', fg='white')
        self.replace_button.pack(side=tk.LEFT, padx=5)

    def create_menus(self):
        menubar = tk.Menu(self.top_level)  # Changed to top_level
        self.top_level.config(menu=menubar)  # Changed to top_level

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Open', command=self.open_file_dialog)
        file_menu.add_command(label='Save', command=self.save_file_dialog)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.master.destroy)
        menubar.add_cascade(label='File', menu=file_menu)

        validate_menu = tk.Menu(menubar, tearoff=0)
        validate_menu.add_command(label='Validate', command=self.validate_content)
        menubar.add_cascade(label='Validate', menu=validate_menu)

    def validate_content(self):
        is_valid = self.ini_parser.validate_ini(self.ini_text.get("1.0", tk.END))
        if is_valid:
            messagebox.showinfo("Success", "INI content is valid!")
            self.status_label.config(text="INI content is valid")
        else:
            messagebox.showerror("Error", "INI content is invalid!")
            self.status_label.config(text="Invalid INI content")

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.ini_text.delete("1.0", tk.END)
                self.ini_text.insert(tk.INSERT, content)
                self.syntax_highlighter.apply(content)  # Adjusted to your actual syntax highlighter method
            self.status_label.config(text=f"Opened file: {file_path}")

    def save_file_dialog(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".ini")
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.ini_text.get("1.0", tk.END))
            self.status_label.config(text=f"Saved file: {file_path}")

    def undo(self):
        try:
            self.ini_text.edit_undo()
        except tk.TclError:
            pass

    def redo(self):
        try:
            self.ini_text.edit_redo()
        except tk.TclError:
            pass

    def search_text(self):
        search_for = simpledialog.askstring("Search", "Enter text to search:")
        if search_for:
            start = "1.0"
            while True:
                pos = self.ini_text.search(search_for, start, stopindex=tk.END)
                if not pos:
                    break
                end = f"{pos}+{len(search_for)}c"
                self.ini_text.tag_add('search', pos, end)
                self.ini_text.tag_config('search', foreground='white', background='blue')
                start = end

    def replace_text(self):
        search_for = simpledialog.askstring("Replace", "Find what:")
        replace_with = simpledialog.askstring("Replace", "Replace with:")
        if search_for and replace_with:
            content = self.ini_text.get("1.0", tk.END)
            updated_content = content.replace(search_for, replace_with)
            self.ini_text.delete("1.0", tk.END)
            self.ini_text.insert(tk.INSERT, updated_content)

if __name__ == "__main__":
    root = tk.Tk()
    app = INIEditor(root)
    root.mainloop()

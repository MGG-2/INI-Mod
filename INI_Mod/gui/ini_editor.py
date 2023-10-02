import tkinter as tk
from tkinter import ttk, simpledialog, filedialog, messagebox
from PIL import Image, ImageTk
import os
from INI_Mod.gui.syntax_highlighter import SyntaxHighlighter
from INI_Mod.utils.ini_parser import IniParser

class INIEditor:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()
        self.create_menus()

        self.ini_parser = IniParser()
        self.syntax_highlighter = SyntaxHighlighter(self.frame)
        self.ini_text = self.syntax_highlighter.text_widget

        # Custom styling
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#2e2e2e")
        self.style.configure("TLabel", background="#2e2e2e", foreground="#ffffff")
        self.style.configure("TButton", background="#333333", foreground="#ffffff")
        self.ini_text.config(bg="#333333", fg="#ffffff", insertbackground="white")

    def create_widgets(self):
        self.status_label = ttk.Label(self.frame, text="Welcome to INI-Mod", anchor=tk.W)
        self.status_label.pack(fill=tk.BOTH)

        self.toolbar = ttk.Frame(self.frame)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Load and display icons on the toolbar buttons
        icons = ["new_icon.png", "open_icon.png", "save_icon.png", "undo_icon.png", "redo_icon.png"]
        commands = [self.new_file, self.open_file_dialog, self.save_file_dialog, self.undo, self.redo]
        for icon, command in zip(icons, commands):
            if os.path.exists(icon):
                img = Image.open(icon)
                img = img.resize((20, 20))
                img = ImageTk.PhotoImage(img)
                btn = ttk.Button(self.toolbar, image=img, command=command)
                btn.image = img
                btn.pack(side=tk.LEFT, padx=2)

        self.button_frame = ttk.Frame(self.frame)
        self.button_frame.pack(fill=tk.X, side=tk.BOTTOM)

        buttons = [('Search', self.search_text), ('Replace', self.replace_text)]
        for text, command in buttons:
            button = tk.Button(self.button_frame, text=text, command=command, bg='#444', fg='white', font=('Arial', 10))
            button.pack(side=tk.LEFT, padx=5)

        self.line_numbers = tk.Text(self.frame, width=5, bg="#2e2e2e", fg="#ffffff", state="disabled")
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        self.ini_text.bind("<KeyRelease>", self.update_line_numbers)
        self.ini_text.bind("<MouseWheel>", self.update_line_numbers)

        self.status_label.config(font=("Arial", 10))
        self.ini_text.bind("<Motion>", self.update_status_bar)

    def create_menus(self):
        top_level = self.master.winfo_toplevel()
        menubar = tk.Menu(top_level, bg="#333333", fg="#ffffff")
        top_level.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0, bg="#333333", fg="#ffffff")
        file_menu.add_command(label='Open', command=self.open_file_dialog)
        file_menu.add_command(label='Save', command=self.save_file_dialog)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.master.destroy)
        menubar.add_cascade(label='File', menu=file_menu)

        validate_menu = tk.Menu(menubar, tearoff=0, bg="#333333", fg="#ffffff")
        validate_menu.add_command(label='Validate', command=self.validate_content)
        menubar.add_cascade(label='Validate', menu=validate_menu)

    def update_line_numbers(self, event=None):
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", tk.END)
        total_lines = self.ini_text.index("@%d,%d" % (self.master.winfo_width(), self.master.winfo_height())).split('.')[0]
        line_numbers = "\n".join(str(no) for no in range(1, int(total_lines) + 1))
        self.line_numbers.insert("1.0", line_numbers)
        self.line_numbers.config(state="disabled")

    def update_status_bar(self, event=None):
        line, col = self.ini_text.index(tk.INSERT).split(".")
        self.status_label.config(text=f"Line {line}, Column {col}")

    def new_file(self):
        self.ini_text.delete("1.0", tk.END)
        self.status_label.config(text="New file")

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
                self.syntax_highlighter.apply_syntax_highlighting()  # Added this line to apply syntax highlighting when a file is opened
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
import tkinter as tk
import os  # Import os module to handle file paths for icons
from tkinter import ttk, simpledialog, filedialog, messagebox
from INI_Mod.gui.syntax_highlighter import SyntaxHighlighter
from INI_Mod.utils.ini_parser import IniParser
from PIL import Image, ImageTk

class INIEditor:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()
        self.create_menus()

        self.ini_parser = IniParser()
        self.syntax_highlighter = SyntaxHighlighter(self.frame)
        self.ini_text = self.syntax_highlighter.text_widget  # Use the text widget from SyntaxHighlighter

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
            img = Image.open(icon)
            img = img.resize((20, 20))
            img = ImageTk.PhotoImage(img)
            btn = ttk.Button(self.toolbar, image=img, command=command)
            btn.image = img  # Keep a reference to the image object to prevent it from being garbage collected
            btn.pack(side=tk.LEFT, padx=2)

            # Enhance the toolbar with icons and styles
        icons_path = "path_to_your_icons_folder"  # Update with the actual path to your icons

        undo_icon = tk.PhotoImage(file=os.path.join(icons_path, "undo.png"))
        self.undo_button = tk.Button(self.frame, image=undo_icon, command=self.undo)
        self.undo_button.image = undo_icon  # Keep a reference to the image object to avoid garbage collection
        self.undo_button.pack(side=tk.LEFT, padx=5)

        redo_icon = tk.PhotoImage(file=os.path.join(icons_path, "redo.png"))
        self.redo_button = tk.Button(self.frame, image=redo_icon, command=self.redo)
        self.redo_button.image = redo_icon
        self.redo_button.pack(side=tk.LEFT, padx=5)

        self.button_frame = ttk.Frame(self.frame)
        self.button_frame.pack(fill=tk.X, side=tk.BOTTOM)

        buttons = [('Undo', self.undo), ('Redo', self.redo), ('Search', self.search_text), ('Replace', self.replace_text)]
        for text, command in buttons:
            button = tk.Button(self.button_frame, text=text, command=command, bg='#444', fg='white', font=('Arial', 10))
            button.pack(side=tk.LEFT, padx=5)

        self.line_numbers = tk.Text(self.frame, width=5, bg="#2e2e2e", fg="#ffffff", state="disabled")
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        self.ini_text.bind("<KeyRelease>", self.update_line_numbers)
        self.ini_text.bind("<MouseWheel>", self.update_line_numbers)

        self.status_label.config(font=("Arial", 10))
        self.ini_text.bind("<Motion>", self.update_status_bar)

        # Create a status bar
        self.status_bar = tk.Label(self.frame, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Create a Canvas for line numbers
        self.line_number_canvas = tk.Canvas(self.frame, width=30, bg='grey')
        self.line_number_canvas.pack(side=tk.LEFT, fill=tk.Y)

        # Update the line numbers as the text changes
        self.ini_text.bind("<Key>", self.update_line_numbers)
        self.ini_text.bind("<MouseWheel>", self.update_line_numbers)

    def update_status_bar(self, event=None):
        line, col = self.ini_text.index(tk.INSERT).split(".")
        self.status_label.config(text=f"Line {line}, Column {col}")

    def new_file(self):
        self.ini_text.delete("1.0", tk.END)
        self.status_label.config(text="New file")

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
        self.line_number_canvas.delete("all")
        i = self.ini_text.index("@0,0")
        while True:
            dline = self.ini_text.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.line_number_canvas.create_text(2, y, anchor="nw", text=linenum, fill="white")
            i = self.ini_text.index("%s+1line" % i)

    def apply_syntax_highlighting(self, *args):
        # ... (previous code)

        # Improve syntax highlighting
        self.ini_text.tag_configure("section", foreground="orange", font=("Arial", 12, "bold"))
        self.ini_text.tag_configure("key", foreground="white")
        self.ini_text.tag_configure("value", foreground="cyan")

        content = self.ini_text.get("1.0", tk.END)
        self.ini_text.delete("1.0", tk.END)

        # Apply custom syntax highlighting
        for line in content.split("\n"):
            if line.strip().startswith("[") and line.strip().endswith("]"):
                self.ini_text.insert(tk.INSERT, line + "\n", "section")
            else:
                if "=" in line:
                    key, value = line.split("=", 1)
                    self.ini_text.insert(tk.INSERT, key, "key")
                    self.ini_text.insert(tk.INSERT, "=")
                    self.ini_text.insert(tk.INSERT, value + "\n", "value")
                else:
                    self.ini_text.insert(tk.INSERT, line + "\n")

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
                self.status_bar.config(text=f"Opened file: {file_path}")

    def save_file_dialog(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".ini")
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.ini_text.get("1.0", tk.END))
                self.status_label.config(text=f"Saved file: {file_path}")
                self.status_bar.config(text=f"Saved file: {file_path}")

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

from .syntax_highlighter import SyntaxHighlighter
import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
import configparser
from tkinter import messagebox

class INIEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("INI File Editor")
        
        self.ini_text = tk.Text(root, wrap=tk.WORD)
        self.ini_text.pack(fill=tk.BOTH, expand=True)
        # Create a menu bar
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)
        
        # Create a File menu
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open INI File", command=self.open_ini_file)
        self.file_menu.add_command(label="Save INI File", command=self.save_ini_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

        # Create a context menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self.copy_text)
        self.ini_text.bind("<Button-3>", self.show_context_menu)

        # Create Undo and Redo buttons
        self.undo_button = tk.Button(root, text="Undo", command=self.undo)
        self.undo_button.pack(side=tk.LEFT, padx=5)
        self.redo_button = tk.Button(root, text="Redo", command=self.redo)
        self.redo_button.pack(side=tk.LEFT, padx=5)

        # Create a Syntax Highlighting toggle button
        self.syntax_highlighting_enabled = tk.BooleanVar(value=True)
        self.highlighting_button = tk.Checkbutton(root, text="Enable Syntax Highlighting",
                                                  variable=self.syntax_highlighting_enabled, command=self.toggle_syntax_highlighting)
        self.highlighting_button.pack()

        # Create a text widget to display INI content
        self.ini_text = tk.Text(root, wrap=tk.WORD)
        self.ini_text.pack(fill=tk.BOTH, expand=True)
        
    def open_ini_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("INI Files", "*.ini")])
        if file_path:
            config = configparser.ConfigParser()
            try:
                config.read(file_path)
            except configparser.Error as e:
                # Handle INI parsing errors
                messagebox.showerror("INI Parsing Error", f"Error reading INI file: {e}")
                return
            ini_content = "\n".join([f"{section}:\n{dict(config[section])}" for section in config.sections()])
            self.ini_text.delete(1.0, tk.END)
            self.ini_text.insert(tk.END, ini_content)
    
    def save_ini_file(self):
        file_path = filedialog.asksaveasfilename(filetypes=[("INI Files", "*.ini")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.ini_text.get(1.0, tk.END))

    def toggle_syntax_highlighting(self):
        if self.syntax_highlighting_enabled.get():
            self.highlight_syntax()
        else:
            self.ini_text.tag_remove("syntax", "1.0", tk.END)

    def highlight_syntax(self):
        # Implement your syntax highlighting logic here
        pass

    def copy_text(self):
        selected_text = self.ini_text.get(tk.SEL_FIRST, tk.SEL_LAST)
        self.root.clipboard_clear()
        self.root.clipboard_append(selected_text)

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def undo(self):
        self.ini_text.edit_undo()

    def redo(self):
        self.ini_text.edit_redo()

if __name__ == "__main__":
    root = tk.Tk()
    app = INIEditor(root)
    root.mainloop()

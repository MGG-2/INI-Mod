import tkinter as tk
from tkinter import filedialog, messagebox  # Added missing imports
from INI_Mod.gui.syntax_highlighter import SyntaxHighlighter
from INI_Mod.utils.ini_parser import IniParser
from ttkthemes import ThemedTk

class INIEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("INI File Editor")
        
        self.ini_text = tk.Text(self.master, wrap=tk.WORD)
        self.ini_text.pack(fill=tk.BOTH, expand=True)

        # Change the theme
        self.theme = ThemedTk(theme="arc")

        # Creating a menu bar
        menubar = tk.Menu(master)
        master.config(menu=menubar)
        
        self.status_label = tk.Label(master, text="Welcome to INI-Mod", anchor=tk.W)
        self.status_label.pack(fill=tk.BOTH)

        # Creating a file menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Open', command=self.open_file_dialog)
        file_menu.add_command(label='Save', command=self.save_file_dialog)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.master.destroy)
        menubar.add_cascade(label='File', menu=file_menu)

        # Creating a validate menu
        validate_menu = tk.Menu(menubar, tearoff=0)
        validate_menu.add_command(label='Validate', command=self.validate_content)
        menubar.add_cascade(label='Validate', menu=validate_menu)

        # Create a context menu
        self.context_menu = tk.Menu(self.master, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self.copy_text)
        self.ini_text.bind("<Button-3>", self.show_context_menu)

        # Create Undo and Redo buttons
        self.undo_button = tk.Button(self.master, text="Undo", command=self.undo)
        self.undo_button.pack(side=tk.LEFT, padx=5)
        self.redo_button = tk.Button(self.master, text="Redo", command=self.redo)
        self.redo_button.pack(side=tk.LEFT, padx=5)

        # Create a Syntax Highlighting toggle button
        self.syntax_highlighting_enabled = tk.BooleanVar(value=True)
        self.highlighting_button = tk.Checkbutton(self.master, text="Enable Syntax Highlighting",
        variable=self.syntax_highlighting_enabled, command=self.toggle_syntax_highlighting)
        self.highlighting_button.pack()

        # Create a text widget to display INI content
        self.ini_text = tk.Text(self.master, wrap=tk.WORD)
        self.ini_text.pack(fill=tk.BOTH, expand=True)
        
        self.highlighter = SyntaxHighlighter(self.ini_text)
    def open_ini_file(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.INSERT, content)
            self.highlighter.apply_syntax_highlighting()  # Add this line to apply syntax highlighting

    def save_ini_file(self, file_path):
        try:
            content = self.text_widget.get(1.0, tk.END)
            with open(file_path, 'w') as file:
                file.write(content)
            messagebox.showinfo("Success", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {e}")

    def validate_ini_content(self):
        content = self.text_widget.get(1.0, tk.END)
        parser = IniParser()
        is_valid = parser.validate_ini(content)
        return is_valid

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
        self.master.clipboard_clear()
        self.master.clipboard_append(selected_text)

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def undo(self):
        self.ini_text.edit_undo()

    def redo(self):
        self.ini_text.edit_redo()

    def open_file_dialog(self):
        try:
            file_path = filedialog.askopenfilename()
            if file_path:
                self.open_ini_file(file_path)
                self.status_label.config(text=f"Opened file: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while opening the file: {e}")
            self.status_label.config(text="Error opening file")

    def save_file_dialog(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".ini")
            if file_path:
                self.save_ini_file(file_path)
                self.status_label.config(text=f"Saved file: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {e}")
            self.status_label.config(text="Error saving file")
            
    def validate_content(self):
        try:
            is_valid = self.validate_ini_content()
            if is_valid:
                messagebox.showinfo("Success", "INI content is valid!")
                self.status_label.config(text="INI content is valid")
            else:
                messagebox.showerror("Error", "INI content is invalid!")
                self.status_label.config(text="Invalid INI content")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while validating the content: {e}")
            self.status_label.config(text="Error validating content")

if __name__ == "__main__":
    root = ThemedTk(theme="arc")  # Changed to ThemedTk and set theme here
    app = INIEditor(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk, simpledialog, filedialog, messagebox
from PIL import Image, ImageTk
import os
from INI_Mod.gui.syntax_highlighter import SyntaxHighlighter
from INI_Mod.utils.ini_parser import IniParser

class INIEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("INI-Mod Editor")
        self.master.geometry("800x600")
        self.master.configure(bg="#1f1f1f")
    
        self.frame = ttk.Frame(self.master)  # Create the frame here
        self.frame.pack(fill=tk.BOTH, expand=True)
    
        self.ini_text = None  # Initialize ini_text attribute
    
        self.create_widgets()
        self.create_menus()
    
        self.ini_parser = IniParser()
        self.syntax_highlighter = SyntaxHighlighter(self.frame)
    
        # Initialize self.ini_text after SyntaxHighlighter
        self.ini_text = self.syntax_highlighter.text_widget
    
        # Bind the event handler after creating self.ini_text
        self.ini_text.bind("<Motion>", self.update_status_bar)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.toolbar = ttk.Frame(self.frame)
        self.toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5, anchor="w")

        icons = ["new_icon.png", "open_icon.png", "save_icon.png", "undo_icon.png", "redo_icon.png"]
        commands = [self.new_file, self.open_file_dialog, self.save_file_dialog, self.undo, self.redo]
        tooltips = ["New File", "Open File", "Save File", "Undo", "Redo"]

        for icon, command, tooltip in zip(icons, commands, tooltips):
            if os.path.exists(icon):
                img = Image.open(icon)
                img = img.resize((24, 24))
                img = ImageTk.PhotoImage(img)
                btn = ttk.Button(self.toolbar, image=img, command=command, style="Toolbar.TButton")
                btn.image = img
                btn.pack(side=tk.LEFT, padx=5)
                self.add_tooltip(btn, tooltip)

        self.status_label = ttk.Label(self.frame, text="Line 1, Column 1", anchor=tk.W, font=("Arial", 10))
        self.status_label.pack(fill=tk.BOTH, side=tk.BOTTOM, padx=5, pady=5)

        self.line_numbers = tk.Text(
            self.frame, width=5, bg="#1f1f1f", fg="#ffffff", state="disabled", bd=0, highlightthickness=0
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        self.ini_text.bind("<KeyRelease>", self.update_line_numbers)
        self.ini_text.bind("<MouseWheel>", self.update_line_numbers)

        self.update_status_bar()

        # Configure the appearance of the main text editor
        self.ini_text.configure(font=("Courier New", 12), insertbackground="white")
        self.ini_text.config(selectbackground="blue", selectforeground="white")
        

    def create_widgets(self):
        # Modify the appearance of widgets, if needed
        self.status_label = ttk.Label(self.frame, text="Welcome to INI-Mod", anchor=tk.W, font=("Arial", 14, "bold"))
        self.status_label.pack(fill=tk.BOTH)

        self.toolbar = ttk.Frame(self.frame)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.button_frame = ttk.Frame(self.frame)
        self.button_frame.pack(fill=tk.X, side=tk.BOTTOM)

        buttons = [('Search', self.search_text), ('Replace', self.replace_text)]
        for text, command in buttons:
            button = tk.Button(
                self.button_frame, text=text, command=command, bg='#666', fg='white', font=('Arial', 12, "bold")
            )
            button.pack(side=tk.LEFT, padx=10)

        self.status_label.config(font=("Arial", 12, "bold"))
        self.ini_text.bind("<Motion>", self.update_status_bar)

    def add_tooltip(self, widget, text):
        """
        Create a tooltip for a given widget
        """
        widget.bind("<Enter>", lambda event, text=text: self.show_tooltip(event, text))
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event, text):
        """
        Display the tooltip when hovering over a widget
        """
        x, y, _, _ = event.widget.bbox("insert")
        x += event.widget.winfo_rootx() + 25
        y += event.widget.winfo_rooty() + 20
        self.tooltip = ttk.Label(self.master, text=text, background="#333333", foreground="#ffffff")
        self.tooltip.place(x=x, y=y, anchor="nw")

    def hide_tooltip(self, event):
        """
        Hide the tooltip when the mouse leaves the widget
        """
        self.tooltip.destroy()

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
        # Enhanced line number update function
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", tk.END)
        total_lines = self.ini_text.index("@%d,%d" % (self.master.winfo_width(), self.master.winfo_height())).split('.')[0]
        line_numbers = "\n".join(str(no) for no in range(1, int(total_lines) + 1))
        self.line_numbers.insert("1.0", line_numbers)
        self.line_numbers.config(state="disabled")

    def update_status_bar(self, event=None):
        # Enhanced status bar update function
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

class CreateToolTip(object):
    """
    Create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.onEnter)
        self.widget.bind("<Leave>", self.onLeave)
        self.widget.bind("<ButtonPress>", self.onLeave)
        self.id = None
        self.tw = None

    def onEnter(self, event=None):
        self.schedule()

    def onLeave(self, event=None):
        self.unschedule()
        self.hide()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.show)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def show(self, event=None):
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tw, text=self.text, justify='left',
                      background="#ffffff", relief='solid', borderwidth=1,
                      wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hide(self):
        if self.tw:
            self.tw.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = INIEditor(root)
    root.mainloop()

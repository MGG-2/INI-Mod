import tkinter as tk
from tkinter import OptionMenu, StringVar
from pygments import highlight
from pygments.lexers import IniLexer
from pygments.formatters import TerminalFormatter  # Changed to TerminalFormatter for compatibility
from pygments.styles import get_all_styles

class SyntaxHighlighter:
    def __init__(self, frame):
        self.frame = frame
        self.text_widget = tk.Text(self.frame, wrap=tk.WORD, bg='#2e2e2e', fg='#ffffff', insertbackground='white')
        self.text_widget.pack(fill=tk.BOTH, expand=True)

        # Adding a dropdown menu for selecting syntax highlighting themes
        self.style_var = StringVar()
        self.style_var.set("default")  # default value
        styles = list(get_all_styles())
        self.option_menu = OptionMenu(self.frame, self.style_var, *styles)
        self.option_menu.pack(side=tk.LEFT, padx=5)
        self.style_var.trace('w', self.apply_syntax_highlighting)

    def apply_syntax_highlighting(self, *args):
        ini_content = self.text_widget.get(1.0, tk.END)
        selected_style = self.style_var.get()
        formatter = TerminalFormatter(style=selected_style)  # Changed to TerminalFormatter for compatibility
        highlighted_content = highlight(ini_content, IniLexer(), formatter)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.INSERT, highlighted_content)

        # Customizing the syntax highlighting styles
        self.text_widget.tag_configure("section", foreground="orange", font=("Arial", 12, "bold"))
        self.text_widget.tag_configure("key", foreground="white")
        self.text_widget.tag_configure("value", foreground="cyan")

        # Applying the syntax highlighting
        content = self.text_widget.get("1.0", tk.END)
        self.text_widget.delete("1.0", tk.END)

        for line in content.split("\n"):
            if line.strip().startswith("[") and line.strip().endswith("]"):
                self.text_widget.insert(tk.INSERT, line + "\n", "section")
            else:
                if "=" in line:
                    key, value = line.split("=", 1)
                    self.text_widget.insert(tk.INSERT, key, "key")
                    self.text_widget.insert(tk.INSERT, "=")
                    self.text_widget.insert(tk.INSERT, value + "\n", "value")
                else:
                    self.text_widget.insert(tk.INSERT, line + "\n")

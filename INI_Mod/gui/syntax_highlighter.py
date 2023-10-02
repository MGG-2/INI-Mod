import tkinter as tk
from tkinter import scrolledtext, OptionMenu, StringVar
from pygments import highlight
from pygments.lexers import IniLexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_all_styles

class SyntaxHighlighter:
    def __init__(self, frame):
        self.frame = frame
        self.text_widget = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD)
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        self.text_widget.config(bg='#2e2e2e', fg='white', insertbackground='white')  # Set dark background and white text

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
        formatter = HtmlFormatter(style=selected_style)
        highlighted_content = highlight(ini_content, IniLexer(), formatter)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.INSERT, highlighted_content)
        self.text_widget.tag_config('Token.Name', foreground='#FFD700')  # Example of setting color for a specific token
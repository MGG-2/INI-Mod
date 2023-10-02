import tkinter as tk
from tkinter import scrolledtext
from pygments import highlight
from pygments.lexers import IniLexer
from pygments.formatters import HtmlFormatter

class SyntaxHighlighter:
    def __init__(self, tab):
        self.tab = tab
        self.text_widget = scrolledtext.ScrolledText(self.tab, wrap=tk.WORD)
        self.text_widget.pack(fill=tk.BOTH, expand=True)
    
    def apply_syntax_highlighting(self):
        ini_content = self.text_widget.get(1.0, tk.END)
        highlighted_ini = highlight(ini_content, IniLexer(), HtmlFormatter())
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, highlighted_ini)
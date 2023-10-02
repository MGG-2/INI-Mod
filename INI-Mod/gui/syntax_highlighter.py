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
        # Get the current content from the text widget
        ini_content = self.text_widget.get(1.0, tk.END)

        # Highlight the INI content using Pygments
        highlighted_content = highlight(ini_content, IniLexer(), HtmlFormatter())

        # Clear the text widget
        self.text_widget.delete(1.0, tk.END)

        # Insert the highlighted content back into the text widget
        self.text_widget.insert(tk.INSERT, highlighted_content)

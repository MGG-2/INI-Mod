import tkinter as tk
from pygments import highlight
from pygments.lexers import IniLexer
from pygments.formatters import HtmlFormatter  # Changed to HtmlFormatter for better compatibility
from pygments.styles import get_all_styles
import re

class SyntaxHighlighter:
    def __init__(self, frame):
        self.frame = frame
        self.text_widget = tk.Text(self.frame, wrap=tk.WORD, bg='#2e2e2e', fg='#ffffff', insertbackground='white')
        self.text_widget.pack(fill=tk.BOTH, expand=True)

        self.text_widget.bind("<KeyRelease>", self.on_key_release)

    def on_key_release(self, event=None):
        ini_content = self.text_widget.get(1.0, tk.END)
        highlighted_content = highlight(ini_content, IniLexer(), HtmlFormatter(style="monokai", nowrap=True))

        # Extracting only the text content from the HTML output
        text_only = re.sub(r"<[^>]+>", "", highlighted_content)

        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.INSERT, text_only)

        # You can add more custom tags and styles as per your requirements
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

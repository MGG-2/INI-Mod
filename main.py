import tkinter as tk
from tkinter import ttk
from gui.ini_editor import INIEditor
from ttkthemes import ThemedTk
from INI_Mod.gui.ini_editor import INIEditor

def main():
    root = ThemedTk(theme="breeze")  # Set the theme to "breeze"
    app = INIEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
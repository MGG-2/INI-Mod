from tkinter import ttk
from ttkthemes import ThemedTk
from gui.ini_editor import INIEditor

def main():
    root = ThemedTk(theme="breeze")  # Set the theme to "breeze"
    app = INIEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()

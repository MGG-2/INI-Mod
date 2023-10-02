import argparse
import tkinter as tk
from tkinter import ttk, messagebox
from INI_Mod.gui.ini_editor import INIEditor

def main(file_path=None):
    try:
        root = tk.Tk()
        tab_control = ttk.Notebook(root)
        tab1 = ttk.Frame(tab_control)
        tab_control.add(tab1, text='INI Editor')
        tab_control.pack(expand=1, fill='both')
        ini_editor = INIEditor(tab1)

        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                ini_editor.set_content(content)

        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='INI File Editor')
    parser.add_argument('--file', type=str, help='Path to the INI file to open')
    args = parser.parse_args()
    main(file_path=args.file)

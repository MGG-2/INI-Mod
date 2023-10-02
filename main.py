import argparse
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from INI_Mod.gui.ini_editor import INIEditor
import traceback  # Import the traceback module

def main(file_path=None):
    try:
        root = ThemedTk(theme="yaru")  # Changed to a dark theme
        ini_editor = INIEditor(root)

        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                ini_editor.ini_text.delete("1.0", tk.END)
                ini_editor.ini_text.insert(tk.INSERT, content)

        root.mainloop()
    except Exception as e:
        error_message = f"An error occurred: {e}\n{traceback.format_exc()}"  # Print the full traceback
        print(error_message)  # Print error to the console
        messagebox.showerror("Error", error_message)  # Show error in a messagebox

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='INI File Editor')
    parser.add_argument('--file', type=str, help='Path to the INI file to open')
    args = parser.parse_args()
    main(file_path=args.file)

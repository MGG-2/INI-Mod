import argparse
import customtkinter
import tkinter as tk
from tkinter import messagebox
from INI_Mod.gui.ini_editor import INIEditor  # Make sure this import path is correct
import traceback

def main(file_path=None):
    try:
        ini_editor = INIEditor()  # Create an instance of INIEditor

        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()

                # Create a new tab for the opened file
                tab = tk.Text(ini_editor.notebook, bg="#2e2e2e", fg="#ffffff")
                tab.insert(tk.END, content)
                ini_editor.notebook.add(tab, text="Opened File")

                # Update the status bar
                ini_editor.status_bar.config(text=file_path)

        ini_editor.mainloop()  # Start the main loop of INIEditor
    except Exception as e:
        error_message = f"An error occurred: {e}\n{traceback.format_exc()}"
        print(error_message)
        messagebox.showerror("Error", error_message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='INI File Editor')
    parser.add_argument('--file', type=str, help='Path to the INI file to open')
    args = parser.parse_args()
    main(file_path=args.file)

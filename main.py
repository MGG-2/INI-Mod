import argparse
import logging
import tkinter as tk
from tkinter import messagebox
from INI_Mod.gui.ini_editor import INIEditor  # Ensure this import path is correct
import traceback

logging.basicConfig(level=logging.DEBUG)


def main(file_path=None):
    try:
        ini_editor = INIEditor()  # Create an instance of INIEditor

        if file_path:
            try:
                logging.info(f"Attempting to load INI file at {file_path}")
                ini_editor.load_ini_file(file_path)
                logging.info("INI file loaded successfully.")
            except Exception as e:
                logging.error(f"Failed to load the INI file at {file_path}: {e}")
                messagebox.showerror("Error", f"Failed to load the INI file at {file_path}.\nError: {e}")
            else:
                if ini_editor.tab_view is None or not ini_editor.tab_view.winfo_exists():
                    logging.error("Tab view not created or not visible.")
                else:
                    logging.info("Tab view created and visible.")

        ini_editor.mainloop()  # Start the main loop of INIEditor
    except Exception as e:
        error_message = f"An error occurred: {e}\n{traceback.format_exc()}"
        logging.error(error_message)
        messagebox.showerror("Error", error_message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='INI File Editor')
    parser.add_argument('--file', type=str, help='Path to the INI file to open')
    args = parser.parse_args()

    main(file_path=args.file)

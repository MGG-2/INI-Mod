import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from INI_Mod.utils.ini_parser import IniParser
import logging

logging.basicConfig(level=logging.DEBUG)


class INIEditor(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.parser = IniParser()
        self.title("INI Editor")
        self.geometry("1100x580")

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.configure_grid()
        self.sidebar = self.create_sidebar()
        self.tab_view = None

    def configure_grid(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Adjusted this line to set weight to 0
        self.grid_rowconfigure(1, weight=2)

    def create_sidebar(self):
        
        sidebar = ctk.CTkFrame(self)
        sidebar.grid(row=0, column=0, rowspan=3, sticky="nsew")  # Adjusted rowspan to 3
        sidebar.grid_rowconfigure(3, weight=1)  # Adjusted this line to set rowconfigure to 3

        ctk.CTkLabel(sidebar, text="INI Editor").grid(row=0, column=0, padx=20, pady=(20, 10))
        ctk.CTkButton(sidebar, text="Open INI File", command=self.open_ini_file).grid(row=1, column=0, padx=20, pady=10)
        ctk.CTkButton(sidebar, text="Save INI File", command=self.save_ini_file).grid(row=2, column=0, padx=20, pady=10)

        return sidebar

    def create_tab_view(self):
        if self.tab_view is not None:
            self.tab_view.destroy()

        tab_view = ctk.CTkTabview(self)
        tab_view.grid(row=0, column=1, sticky="nsew", padx=(50, 50), pady=(20, 20))  # Adjusted this line to set row to 0
        return tab_view

    def open_ini_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".ini",
                                               filetypes=[("INI files", "*.ini"), ("All Files", "*.*")])
        if file_path:
            self.load_ini_file(file_path)
        else:
            logging.debug("No file selected.")

    def load_ini_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                ini_content = file.read()

            self.parser.parse_ini(ini_content)
            self.tab_view = self.create_tab_view()
            self.populate_tabs()
        except Exception as e:
            logging.error(f"Error loading INI file: {e}")
            messagebox.showerror("Error", "Failed to load the INI file.")

    def categorize_settings(self):
        categories = {
            'Graphics': [],
            'Lighting Settings': [],
            'Miscellaneous': []
        }

        # Mapping of settings to their comments
        comments = {
            # Add the comments for each setting here, for example:
            'r.TextureStreaming': 'Disable texture streaming to load all textures at startup',
            'r.MaxAnisotropy': 'Set the maximum anisotropic filtering level',
            # ... (add all other settings and their comments)
        }

        for section, options in self.parser.sections.items():
            for option, value in options.items():
                category = self.parser.get_category(option)
                if category:
                    comment = comments.get(option, '')  # Get the comment for the setting, if available
                    categories[category].append((section, option, value, comment))

        return categories

    def populate_tabs(self):
        categories = self.categorize_settings()

        for category, settings in categories.items():
            tab = self.tab_view.add(category)

            # Create a scrollable frame inside the tab
            scroll_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
            scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
            scroll_frame.config(highlightthickness=0)

            row = 0
            for section, option, value, comment in settings:
                # Add settings directly to the scrollable frame
                ctk.CTkLabel(scroll_frame, text=f"{option}").grid(row=row, column=0, sticky="w")
                entry = ctk.CTkEntry(scroll_frame)
                entry.insert(0, value)
                entry.grid(row=row, column=1, sticky="ew")
                ctk.CTkLabel(scroll_frame, text=f" {comment}", fg_color="transparent").grid(row=row, column=2, sticky="w")
                row += 1


    def save_ini_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".ini",
                                                filetypes=[("INI files", "*.ini"), ("All Files", "*.*")])
        if file_path:
            self.save_current_state_to_file(file_path)
        else:
            logging.debug("Save operation cancelled.")

    def save_current_state_to_file(self, file_path):
        try:
            content = self.parser.get_ini_content()

            with open(file_path, 'w') as file:
                file.write(content)

            messagebox.showinfo("Success", "File saved successfully.")
        except Exception as e:
            logging.error(f"Error saving INI file: {e}")
            messagebox.showerror("Error", "Failed to save the INI file.")

    def update_option_value(self, section, option, value):
        try:
            self.parser.config.set(section, option, value)
            logging.info(f"Updated {option} in {section} to {value}")
        except Exception as e:
            logging.error(f"Error updating option value: {e}")
            messagebox.showerror("Error", f"Failed to update the option {option} in section {section}.")


if __name__ == "__main__":
    editor = INIEditor()
    editor.mainloop()

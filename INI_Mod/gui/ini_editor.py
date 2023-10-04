
import tkinter as tk
from tkinter import filedialog
import customtkinter
from customtkinter.windows.widgets.ctk_switch import CTkSwitch  # Import the CTkSwitch class
#from INI_Mod.gui.syntax_highlighter import SyntaxHighlighter
from INI_Mod.utils.ini_parser import IniParser

import logging

logging.basicConfig(level=logging.DEBUG)  # Set logging level to DEBUG


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class INIEditor(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.parser = IniParser()
        self.title("INI EDITOR")
        self.geometry(f"{1100}x{580}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="INI EDITOR", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        #self.textbox = customtkinter.CTkTextbox(self, width=250)
        #self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        #self.textbox.configure(state=tk.DISABLED)
        self.textbox = None  # Initialize the textbox as None
        self.switch_frame = None

        self.open_file_button = customtkinter.CTkButton(self.sidebar_frame, text="Open INI File", command=self.open_ini_file)
        self.open_file_button.grid(row=1, column=0, padx=20, pady=10)
        self.save_button = customtkinter.CTkButton(self.sidebar_frame, text="Save INI File", command=self.save_ini_file)
        self.save_button.grid(row=2, column=0, padx=20, pady=10)

        self.buttons_frame = tk.Frame(self, bg=self.cget('bg'))
        self.buttons_frame.grid(row=1, column=1, sticky="nsew")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        # For demonstration, I'm using a hardcoded file path; you should implement a file dialog to select the .ini file
        file_path = 'example.ini'  
        self.load_ini_file(file_path)

    def create_textbox(self):
        if self.textbox is None:
            self.textbox = customtkinter.CTkTextbox(self, width=250)
            self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
            self.textbox.configure(state=tk.DISABLED)

    def open_ini_file(self):
        logging.debug("Opening INI file...")
        file_path = filedialog.askopenfilename(defaultextension=".ini", filetypes=[("INI files", "*.ini"), ("All Files", "*.*")])
        if file_path:
            logging.debug(f"File selected: {file_path}")
            with open(file_path, 'r') as file:
                ini_content = file.read()
                logging.debug("INI content loaded:")
                logging.debug(ini_content)

            self.create_textbox()  # Create the textbox when the file is opened
            self.textbox.configure(state=tk.NORMAL)
            self.textbox.delete("1.0", tk.END)

            special_sections = {}
            current_section = None
            MAX_OPTIONS_FOR_REGULAR_SECTION = 5
            processed_cvars = set()

            for line in ini_content.splitlines():
                if '=' in line:
                    cvar = line.split('=')[0].strip()
                    if cvar in processed_cvars:
                        continue  # Skip the duplicated cvar
                    processed_cvars.add(cvar)

                if line.strip().startswith('[') and line.strip().endswith(']'):
                    if current_section and len(special_sections.get(current_section, [])) > MAX_OPTIONS_FOR_REGULAR_SECTION:
                        button_text = current_section.split('/')[-1].replace('script/', '').replace('.', ' ').title()
                        button = customtkinter.CTkButton(self.buttons_frame, text=button_text, 
                                                         command=lambda c=special_sections[current_section][:]: self.display_special_content(c))
                        button.pack(padx=20, pady=10, fill="x")
                        current_section = None

                    current_section = line.strip()[1:-1]
                    special_sections[current_section] = []

                elif current_section:
                    special_sections[current_section].append(line)

                else:
                    self.textbox.insert(tk.INSERT, line + '\n')
                    self.textbox.configure(state=tk.DISABLED)
                    self.parser.parse_ini(ini_content)
                logging.debug("No file selected.")

    def save_ini_file(self):
        logging.debug("Saving INI file...")
        file_path = filedialog.asksaveasfilename(defaultextension=".ini", filetypes=[("INI files", "*.ini"), ("All Files", "*.*")])
        if file_path:
            logging.debug(f"File will be saved to: {file_path}")
            with open(file_path, 'w') as file:
                content = self.textbox.get("1.0", tk.END)
                file.write(content)
                logging.debug("File saved successfully.")
                logging.debug("Saved content:")
                logging.debug(content)
            print(f"File saved to {file_path}")
        else:
            logging.debug("Save operation cancelled.")
 
    def update_textbox_content(self, option, new_value):
        logging.debug(f"Updating textbox content for option {option} to {new_value}")
        content = self.textbox.get("1.0", tk.END).splitlines()
        updated_content = []
        for line in content:
            if line.strip().startswith(option):
                line = f"{option} = {new_value}"
            updated_content.append(line)

        self.textbox.configure(state=tk.NORMAL)
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert(tk.INSERT, '\n'.join(updated_content))
        self.textbox.configure(state=tk.DISABLED)
        logging.debug("Textbox content updated.")
               
    def switch_get(self, option, switch):
        logging.debug(f"Switching option {option}")
        value = switch.get()
        content = self.textbox.get("1.0", tk.END).splitlines()

        # Print the content before the switch for debugging
        logging.debug("Content before switch:")
        logging.debug("\n".join(content))
    
    # Determine the current value type (integer or boolean)
        is_boolean = None
        for line in content:
            if line.strip().startswith(option):
                is_boolean = 'true' in line.lower() or 'false' in line.lower()
                break
            
        if is_boolean is None:
            print(f"Option {option} not found in content.")
            return
    
        if is_boolean:
            new_value = 'True' if value else 'False'
        else:
            new_value = '1' if value else '0'
    
        self.update_textbox_content(option, new_value)
        logging.debug(f"Updated {option} to {new_value}")

        # Print the content after the switch for debugging
        updated_content = self.textbox.get("1.0", tk.END)
        logging.debug("Content after switch:")
        logging.debug(updated_content)
        
    def display_special_content(self, content):
        if self.switch_frame:
            self.switch_frame.destroy()

        self.switch_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.switch_frame.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.switch_frame.grid_columnconfigure(0, weight=1)

        self.textbox.configure(state=tk.NORMAL)
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert(tk.INSERT, '\n'.join(content))
        self.textbox.configure(state=tk.DISABLED)

        for i, line in enumerate(content):
            if '=' in line:
                option, value = line.split('=')
                option = option.strip()
                value = value.strip().lower()

                switch = CTkSwitch(self.switch_frame)
                switch.grid(row=i, column=0, padx=20, pady=5, sticky="w")

                if value in ['true', '1']:
                    switch.get()
                elif value in ['false', '0']:
                    switch.get()

                switch.bind("<ButtonRelease-1>", lambda e, opt=option, s=switch: self.switch_get(opt, s))
                

if __name__ == "__main__":
    editor = INIEditor()
    editor.mainloop()


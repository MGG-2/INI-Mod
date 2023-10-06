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
            self.create_text_box()
        except Exception as e:
            logging.error(f"Error loading INI file: {e}")
            messagebox.showerror("Error", "Failed to load the INI file.")

    def create_text_box(self):
        self.text_box = ctk.CTkTextbox(self, height=10)  # Adjust the height as needed
        self.text_box.grid(row=1, column=1, sticky="nsew", padx=(50, 50), pady=(0, 20))  # Adjust the padding as needed
        self.text_box.insert(tk.END, "Changes will be displayed here...")
        self.text_box.configure(state=tk.DISABLED)

    def categorize_settings(self):
        categories = {
            'Graphics': [],
            'Lighting Settings': [],
            'Miscellaneous': []
        }

        comments = {
            'r.TextureStreaming': 'Disable texture streaming to load all textures at startup',
            'r.MaxAnisotropy': 'Set the maximum anisotropic filtering level',
            'r.Streaming.PoolSize': 'Set the memory pool size (in MB) for texture streaming',
            'r.PostProcessAAQuality': 'Set the quality of post-process anti-aliasing',
            'r.MotionBlurQuality': 'Disable motion blur effect',
            'r.DepthOfFieldQuality': 'Disable depth of field effect',
            'r.LensFlareQuality': 'Disable lens flare effect',
            'r.EyeAdaptationQuality': 'Disable eye adaptation effect',
            'r.BloomQuality': 'Disable bloom effect',
            'r.MaterialQualityLevel': 'Set the material quality level (0 for low, 1 for high)',
            'r.RefractionQuality': 'Set the quality of refraction effects',
            'r.SSR.Quality': 'Set the quality of screen space reflections',
            'r.RayTracing': 'Disable ray tracing effects',
            'r.GlobalIllumination': 'Disable global illumination effects',
            'r.Tessellation': 'Disable tessellation effects',
            'r.Atmosphere': 'Disable atmosphere effects',
            'r.SkyAtmosphere': 'Disable sky atmosphere effects',
            'r.VolumetricCloud': 'Disable volumetric cloud effects',
            'r.Fog': 'Disable fog effects',
            'r.ShadowQuality': 'Set the overall quality of shadows',
            'r.Shadow.CSM.MaxCascades': 'Set the maximum number of cascades for Cascaded Shadow Maps (CSM)',
            'r.Shadow.RadiusThreshold': 'Set the threshold radius for shadow rendering',
            'r.Shadow.DistanceScale': 'Set the scale factor for shadow distance',
            'r.Shadow.CSM.TransitionScale': 'Set the transition scale for CSM',
            'r.DistanceFieldShadowing': 'Disable distance field shadowing',
            'r.Shadow.MaxResolution': 'Set the maximum resolution for shadows',
            'r.Shadow.MaxCSMResolution': 'Set the maximum resolution for CSM',
            'r.Shadow.PerObject': 'Enable per-object shadow rendering',
            'r.Shadow.FadeExponent': 'Set the fade exponent for shadow fading',
            'r.Shadow.TransitionScale': 'Set the transition scale for shadow transitions',
            'r.LightMaxDrawDistanceScale': 'Set the scale factor for the maximum draw distance of lights',
            'r.CapsuleDirectShadows': 'Disable capsule direct shadows',
            'r.CapsuleIndirectShadows': 'Disable capsule indirect shadows',
            'r.CapsuleMaxDirectOcclusionDistance': 'Set the maximum distance for direct occlusion by capsule shadows',
            'r.CapsuleMaxIndirectOcclusionDistance': 'Set the maximum distance for indirect occlusion by capsule shadows',
            'r.CapsuleShadows': 'Disable capsule shadows',
            'r.LightFunctionQuality': 'Set the quality of light functions',
            'r.TranslucentLightingVolume': 'Disable translucent lighting volume',
            'r.OneFrameThreadLag': 'Enable one frame thread lag to improve performance',
            'r.TriangleOrderOptimization': 'Enable triangle order optimization',
            'r.UniformBufferPooling': 'Enable uniform buffer pooling',
            'r.OptimizeForUAVPerformance': 'Disable optimization for UAV performance',
            'r.InstanceCulling': 'Disable instance culling',
            'r.HairStrands.Cull': 'Disable culling of hair strands',
            'r.HairStrands.Binding': 'Disable binding of hair strands',
            'r.HairStrands.Strands': 'Disable rendering of individual hair strands',
            'r.HairStrands.Cards': 'Disable rendering of hair cards',
            'r.HairStrands.Enable': 'Disable hair strands rendering',
            'r.HairStrands.Simulation': 'Disable simulation of hair strands'
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
                entry.bind("<FocusOut>", lambda event, sec=section, opt=option, ent=entry: self.update_option_value(sec, opt, ent.get()))  # Updated this line
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
            self.text_box.configure(state=tk.NORMAL)
            self.text_box.insert(tk.END, f"\nChanged value for {option} to {value}")  # Added this line to display the change in the text box
            self.text_box.configure(state=tk.DISABLED)
        except Exception as e:
            logging.error(f"Error updating option value: {e}")
            messagebox.showerror("Error", f"Failed to update the option {option} in section {section}.")


if __name__ == "__main__":
    editor = INIEditor()
    editor.mainloop()
import sys
sys.path.append(r'Z:\INI-Mod\INI-Mod\gui')
print(sys.path)  # Add this line to print out sys.path for debugging
from tkinter import ttk
from ttkthemes import ThemedTk
from ini_editor import INIEditor  # This import should work if the path is correct

def main():
    root = ThemedTk(theme="breeze")  # Set the theme to "breeze"
    app = INIEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()

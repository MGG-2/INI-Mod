import sys
sys.path.append('Z:/INI-Mod')
print(sys.path)  # Add this line to print out sys.path for debugging
import unittest
import tkinter as tk
from unittest.mock import patch
from gui.ini_editor import INIEditor

class TestINIEditor(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.ini_editor = INIEditor(self.root)

    @patch('tkinter.filedialog.askopenfilename')
    def test_open_ini_file(self, mock_askopenfilename):
        # Mocking the file dialog to return a specific file path
        mock_askopenfilename.return_value = 'sample.ini'
        
        # Assuming you have a method to get the current content of the text widget
        initial_content = self.ini_editor.get_content()

        self.ini_editor.open_file_dialog()

        # Check if the content has changed after opening a file
        self.assertNotEqual(self.ini_editor.get_content(), initial_content)

    @patch('tkinter.filedialog.asksaveasfilename')
    def test_save_ini_file(self, mock_asksaveasfilename):
        pass# Similar to the above, mock the save file dialog and
        # implement logic to test if the file is saved correctly

    def test_validate_ini_content(self):
        # Set some sample invalid INI content
        self.ini_editor.set_content("[section1]\nkey1")

        # Validate the content
        is_valid = self.ini_editor.validate_ini_content()

        # Check if the validation result is as expected
        self.assertFalse(is_valid)

# More test cases as needed
from pathlib import Path
import win32com.client as win32



class Converter():
    def __init__(self, file_paths):
        self.file_path = file_paths
        self.converted_file_path: Path = self._apply_conversion()

    def _apply_conversion(self):
        # get and apply conversion func
        func = ...
        file_path = ...
        return file_path
            



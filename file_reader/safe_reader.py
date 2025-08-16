from file_reader.registry import get
import tempfile
from pathlib import Path
import shutil as sh
import pandas as pd


class SafeReader():
    def __init__(self, file_path: str):
        self.temp_dir = tempfile.mkdtemp()
        self.file_path = self._temp_path(file_path)
        self.reader_func = get(Path(self.file_path).suffix)
        self.data: pd.DataFrame = self.reader_func(file_path)
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        """Delete tempdir"""
        sh.rmtree(self.temp_dir)

    def _temp_path(self, file_path):
        if self._confirm_path(file_path):
            return self._copy_to_temp(file_path)
        else:
            raise ValueError(f"{file_path} is not a valid file path")

    def _confirm_path(self, file_path):
        
        # is it a string?
        if not isinstance(file_path, str):
            raise TypeError(f"_confirm_path: expected type str, recieved: {type(self.file_path)}")
        
        # if string, is it a valid file path?
        try:
            fp = Path(file_path)
        except Exception as e:
            raise ValueError(f"_confirm_path: invalid file path, {file_path}")
        
        # does the file exist?
        if not fp.exists():
            raise FileExistsError(f"_confirm_path: {fp} does not exist")
        
        # passed all tests, return Path object
        return Path(file_path)

    def _copy_to_temp(self, file_path) -> Path:
        dst_path = Path(self.temp_dir) / Path(file_path).name 
        sh.copy2(file_path, dst_path)
        return Path(dst_path)

    
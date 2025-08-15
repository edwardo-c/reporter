import tempfile
from pathlib import Path
import shutil as sh
import pandas as pd

class SafeReader():
    def __init__(self, file_path: str):
        self.temp_dir = tempfile.mkdtemp()
        self.file_path = self._confirm_path(file_path)
        self.data: pd.DataFrame = self._read_file_path()
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        """Delete tempdir"""
        sh.rmtree(self.temp_dir)

    def _confirm_path(self):

        # is it a string?
        if not isinstance(self.file_path, str):
            raise TypeError(f"_confirm_path: expected type str, recieved: {type(self.file_path)}")
        
        # if string, is it a valid file path?
        try:
            fp = Path(self.file_path)
        except Exception as e:
            raise ValueError(f"_confirm_path: invalid file path, {self.file_path}")

        # passed all tests, return Path object
        return Path(self.file_path)

    def _read_file_path(self):
        
        fp = self._copy_to_temp()

        suffix = self.file_path.suffix

        if suffix == ".csv":
            result = self._safe_read_csv(fp)
        elif suffix == ".xlsx":
            result = self._safe_read_excel(fp)
        else:
            raise TypeError(f"_read_file_path: invalid suffix {suffix}")

        return result

    def _copy_to_temp(self) -> Path:
        dst_path = Path(self.temp_dir) / Path(self.file_path).name 
        sh.copy2(self.file_path, dst_path)
        return Path(dst_path)

    def _safe_read_excel(self, file_path: str | Path, sheet_name=0, header=0, usecols=None, dtype= None) -> pd.DataFrame:
        return pd.read_excel(file_path, sheet_name=sheet_name, header=header, usecols=usecols, dtype=dtype)
    
    def _safe_read_csv(self, file_path: str | Path) -> pd.DataFrame:
        return pd.read_csv(file_path)

    
import shutil
from pathlib import Path
import tempfile
import win32com.client as win32
import pandas as pd

class ForceReader():
    """convert file to xlsx and read"""
    def __init__(self, file_path: Path, cfg: dict = {}):
        self.file_path = file_path
        self.dst_dir = Path(tempfile.mkdtemp())
        self.converted_file: Path = None
        # TODO: implement cfg for non first page reads of dataframe
        # self.cfg = cfg
        self.df: pd.DataFrame | None = None
        self.excel: object = None
        self.wb: object = None
        self.df: pd.DataFrame | None = None

    # TODO: validate file path

    def read_df(self):
        self.convert_to_xlsx()
        self.df = pd.read_excel(self.converted_file)

    def _create_safe_copy(self) -> Path:
        """copies file to temp path, returns temp path"""
        safe_copy = self.dst_dir / self.file_path.name
        shutil.copy2(self.file_path, safe_copy)
        return safe_copy

    def convert_to_xlsx(self):
        """
        converts excel file to xlsx
        """
        # move original to local temp, ensures proper clean up
        safe_copy: Path = self._create_safe_copy()
        try: 
            # open safe local version
            self.wb = self.excel.Workbooks.Open(str(safe_copy))
            # create and store new file path for the CONVERTED copy
            self.converted_file = safe_copy.with_suffix(".xlsx")
            self.wb.SaveAs(Filename=str(self.converted_file), 
                           FileFormat=51) # xlOpenXMLWorkbook
        finally:
            if self.wb:
                self.wb.Close(SaveChanges=False)
            
    def __enter__(self):
        self.excel = win32.gencache.EnsureDispatch("Excel.Application")
        self.excel.Visible = False
        self.excel.DisplayAlerts = False
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.dst_dir.exists():
            shutil.rmtree(self.dst_dir)
        if self.excel: 
            self.excel.Quit()
from contextlib import contextmanager
from pathlib import Path
import win32com.client as win32
import pandas as pd

@contextmanager
def convert_to_xlsx(file_path: Path):
    """converts excel file to xlsx"""
    excel = win32.gencache.Dispatch("Excel.Application")
    try: 
        wb = excel.Workbooks.Open(str(file_path))
        converted_file = file_path.with_suffix(".xlsx")
        wb.SaveAs(
            Filename=str(converted_file), 
            FileFormat=51 # xlOpenXMLWorkbook
        )
        yield converted_file 
    finally:
        if wb:
           wb.Close(SaveChanges=False)
        if excel:
            excel.Quit()

def force_reader(file_path: Path):
    with convert_to_xlsx(file_path) as converted:
        ...
from pathlib import Path
import tempfile

import win32com.client as win32

from file_converter.registry import register_conversion

@register_conversion('xls_to_csv')
def convert_xls_to_csv(cfg: dict):
    """convert xls file to csv and return new file path stored in temp"""
    
    xls_path = cfg['xls_path']
    sheet = cfg['sheet']
    csv_path = cfg.get('csv_path', None) # implement temp csv path

    valid_file_path(xls_path)

    excel = win32.gencache.EnsureDispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False

    try:
        wb = excel.Workbooks.Open(xls_path)
        try:
            # Pick the worksheet
            if sheet is None:
                ws = wb.ActiveSheet
            else:
                ws = wb.Worksheets(sheet)

            # SAFEST pattern: copy the sheet to a new 1-sheet workbook, then SaveAs
            ws.Copy()                         # creates a new workbook as ActiveWorkbook
            temp = excel.ActiveWorkbook
            temp.SaveAs(csv_path, FileFormat=6)
            temp.Close(SaveChanges=False)
        finally:
            wb.Close(SaveChanges=False)
    finally:
        excel.Quit()


def valid_file_path(file_path: str) -> bool:
    """ensure valid file_path"""
    if not isinstance(file_path, str):
        raise TypeError(f"expected type str, recieved {type(file_path)}")

    try:
        path_obj = Path(str)
    except:
        raise ValueError(f"convert_xlx_to_csv: invalid file path, {file_path}")

    if not path_obj.exists():
        raise FileNotFoundError(f"file path {file_path} does not exist")

    return True
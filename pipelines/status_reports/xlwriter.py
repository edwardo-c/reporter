from openpyxl import load_workbook
from pathlib import Path

def generate_reports(template_path: str, sheet_name: str, out_dir: Path,
                     report_map: dict[str, dict[str, float]]):
    """
    Iterate over report map to organize input into apply_cell_map
    args:
        
        template_path: excel template file path
        
        sheet_name: sheet name inside template file
        
        out_dir: directory where all finished files will end
        
        report_map: Range to value map, example:{"A1": 123, "B1": 456}

    """
    for acct_num, cell_map in report_map.items():
        path_out = out_dir / f"{acct_num}.csv"
        _apply_cell_map(path_in=template_path, path_out=path_out, 
                        sheet_name=sheet_name, cell_map=cell_map)

def _apply_cell_map(path_in: str, path_out: Path, 
                    sheet_name: str, cell_map: dict[str, float]):    
    wb = load_workbook(path_in)
    ws = wb[sheet_name]
    for range, val in cell_map.items():
        ws[range].value = val
    wb.save(path_out)
    wb.close()


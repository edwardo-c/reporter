import pandas as pd

from pathlib import Path

class MultipleAdapter:
    def __init__(self):
        pass
    
    @classmethod
    def df(cls, file_path: Path | str, cfg: dict | None = None):

        if isinstance(file_path, str) and Path(file_path).is_file():
            file_path = Path(file_path)

        frames = []

        for c in cfg:
            
            sheet_name = c.get("sheet_name", 0)
            
            header = c.get("header", 0)
            
            df = pd.read_excel(
                io=file_path, 
                sheet_name=sheet_name, 
                header=header
            )

            frames.append(df)

        return pd.concat(frames)

import pandas as pd
from data_toolkit.duckdb.register_frames.factory import CsvFrame, ExcelFrame

class FrameReader():
    def __init__(self):
        self.registry = {
            "xlsx": self._read_xl,
            "xlsm": self._read_xl,
            "csv":  self._read_csv,
        }

    @staticmethod
    def _read_xl(frame: ExcelFrame):
        return pd.read_excel(
            str(frame.path),
            header=frame.header,
            sheet_name=frame.sheet,
        )

    @staticmethod
    def _read_csv(frame: CsvFrame):
        return pd.read_csv(
            str(frame.path),
            header=frame.header,
        )

    def _get_reader(self, kind: str):
        if kind not in self.registry:
            raise KeyError(
                f"invalid frame kind: {kind}. "
                f"see FrameReader.registry for available options"
            )
        else:
            return self.registry[kind]

    def read(self, frame: CsvFrame | ExcelFrame) -> pd.DataFrame:
        reader = self._get_reader(frame.kind)
        
        try:
            df = reader(frame)
        except Exception as e:
            raise ValueError(
                f"Unable to read frame: {frame.register_as}, \n{e}"
            )
        return df

from pathlib import Path
import win32com.client as win32
import tempfile
import shutil as sh
import subprocess

import pandas as pd


class InvalidExt:
    def __init__(self):
        self.xl = None
        self.temp_dir: Path | None = None

    def __enter__(self):
        xl = win32.gencache.EnsureDispatch("Excel.Application")
        xl.DisplayAlerts = False
        xl.Visible = False
        xl.AutomationSecurity = 3  # force disable macros
        self.xl = xl

        self.temp_dir = Path(tempfile.mkdtemp())
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.xl is not None:
            self.xl.Quit()
            self.xl = None

        if self.temp_dir is not None:
            try:
                sh.rmtree(self.temp_dir, ignore_errors=True)
            finally:
                self.temp_dir = None

    def _df(self, file_path: Path) -> pd.DataFrame:
        if self.xl is None or self.temp_dir is None:
            raise RuntimeError(
                "InvalidExt must be used as a context manager or via InvalidExt.df(...)"
            )

        temp_file: Path = self._convert_to_xlsx(file_path)

        # read + always delete the temp file
        try:
            return pd.read_excel(temp_file)
        finally:
            try:
                temp_file.unlink(missing_ok=True)
            except TypeError:
                # For older Python without missing_ok
                if temp_file.exists():
                    temp_file.unlink()

    def _convert_to_xlsx(self, file_path: Path) -> Path:
        wb = None
        xl = self.xl

        # xl must exist here; if not, that's a programming error
        if xl is None or self.temp_dir is None:
            raise RuntimeError("Excel app or temp_dir not initialized")

        try:
            # Unblock the file before Excel touches it
            subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    f'Unblock-File -Path "{str(file_path)}"'
                ],
                check=False,
            )

            wb = xl.Workbooks.Open(str(file_path))
            xlsx_path = self.temp_dir / f"{file_path.stem}.xlsx"
            wb.SaveAs(Filename=str(xlsx_path), FileFormat=51)

            return xlsx_path
        finally:
            if wb is not None:
                wb.Close(SaveChanges=False)

    @classmethod
    def df(cls, file_path: Path) -> pd.DataFrame:
        """Convenience: InvalidExt.df(Path(...)) -> DataFrame"""
        with cls() as conv:
            return conv._df(file_path)

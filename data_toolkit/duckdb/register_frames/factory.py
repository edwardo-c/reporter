from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Any

@dataclass
class CsvFrame():
    kind: str
    path: Path
    header: int
    register_as: str

    @classmethod
    def from_cfg(cls, cfg: Mapping[str, Any]):
        path = cfg["path"]
        register_as = cfg["register_as"]
        header = cfg["header"]

        return cls(
            path=path, 
            header=header, 
            register_as=register_as
        )

@dataclass
class ExcelFrame():
    kind: str
    path: Path
    header: int
    sheet: str
    register_as: str

    @classmethod
    def from_cfg(cls, cfg: Mapping[str, Any]):
        
        path = cfg["path"]
        register_as = cfg["register_as"]
        header = cfg["header"]
        sheet = cfg["sheet"]

        return cls(
            path=path, 
            header=header, 
            sheet=sheet, 
            register_as=register_as
        )

class FrameFactory():
    """
    Frame registry dispatch of data classes
    
    example usage:

        frame_type = FrameRegistry.get_kind("xlsx")

    """
    def __init__(self):
        self.registry = {
            "csv"  : CsvFrame,
            "xlsm" : ExcelFrame,
            "xlsx" : ExcelFrame
        }

    def _get_kind(self, kind_id: str):
        """
        expects normalized kind_id, see ConfigNormalizer
        """
        return self.registry[kind_id]
    
    def make_frame(self, cfg: Mapping[str, str | int | Path]):
        kind = cfg["kind"]
        if kind not in self.registry:
            raise KeyError(
                f"invalid frame kind: {kind}. "
                f"see FrameFactory.registry for available options"
            )
        else:
            frame_kind = self.registry[kind]

        return frame_kind(**cfg)
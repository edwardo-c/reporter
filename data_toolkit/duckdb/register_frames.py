from dataclasses import dataclass, field
import duckdb
from pathlib import Path
import pandas as pd
from typing import Mapping, Any
from data_toolkit.config_reader import validators


@dataclass
class CsvFrame():
    kind: str = "csv"
    path: Path
    header: int
    register_as: str

    @classmethod
    def from_cfg(cls, cfg: Mapping[str, Any]):
        path = validators.get_path(cfg)
        register_as = validators.get_register_as(cfg)
        header = validators.get_header(cfg)

        return cls(
            path=path, 
            header=header, 
            register_as=register_as
        )

@dataclass
class ExcelFrame():
    kind: str = "excel_sheet"
    path: Path
    header: int
    sheet: str
    register_as: str

    @classmethod
    def from_cfg(cls, cfg: Mapping[str, Any]):
        
        path = validators.get_path(cfg)
        register_as = validators.get_register_as(cfg)
        header = validators.get_header(cfg)
        sheet = validators.get_sheet(cfg)

        return cls(
            path=path, 
            header=header, 
            sheet=sheet, 
            register_as=register_as
        )

FRAME_REGISTRY = {
    "csv"  : CsvFrame,
    "xlsm" : ExcelFrame,
    "xlsx" : ExcelFrame
}

def register_from_cfg(cfg, conn):
    """dispatch for frame type registration from config"""
    frame_map = {}
    for raw_frame_cfg in cfg:

        kind = validators.get_kind(raw_frame_cfg, FRAME_REGISTRY)
        
        frame = 

def register_mapping(frame_map: dict, conn):
    """expects alias -> dataframe"""
    for alias, df in frame_map.items():
        pass




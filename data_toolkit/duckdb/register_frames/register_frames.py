from dataclasses import dataclass
import duckdb
import pandas as pd
from pathlib import Path
from typing import Mapping, Any


import logging

logging.basicConfig(level=logging.INFO)

@dataclass
class CsvFrame():
    kind: str
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
    kind: str
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

class FrameRegistry():
    """
    Frame registry dispatch of data classes
    
    example usage:

        frame_type = FrameRegistry.get_kind("xlsx")

    """
    registry = {
        "csv"  : CsvFrame,
        "xlsm" : ExcelFrame,
        "xlsx" : ExcelFrame
    }

    @classmethod
    def get_kind(cls, kind_id: str):
        """
        expects normalized kind_id, see ConfigNormalizer
        """
        return cls.registry[kind_id]

class FrameReader():
    registry = {
        "xlsx": pd.read_excel,
        "xlsm": pd.read_excel,
        "csv":  pd.read_csv,
    }

    @classmethod
    def read(frame: CsvFrame | ExcelFrame):
        ...

def register_frames_from_cfg(cfg, conn):
    """dispatch frame registration from config"""

    for frame_id, frame_details in cfg.items():

        logging.info(f"reading frame_id: {frame_id}")
        frame = FrameRegistry.get_kind(frame_details["kind"])

        # normalize config, pass properly formatted inputs to the frame
        frame = ...

def register_mapping(frame_map: dict, conn):
    """expects alias -> dataframe"""
    for alias, df in frame_map.items():
        pass




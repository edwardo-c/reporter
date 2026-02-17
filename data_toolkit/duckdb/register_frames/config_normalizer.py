from pathlib import Path
from typing import Mapping

from utils.validators import (
    validate_path, 
    validate_str, 
    validate_positive_int
)

ALLOW_ZERO_STR = False

class ConfigNormalizer():
    def __init__(self):
        self.registry = {
            "csv": self._process_csv_cfg,
            "xlsx": self._process_xl_cfg,
            "xlsm": self._process_xl_cfg,
        }

    @staticmethod
    def verify_key_existance(key_name: str, raw_cfg):
        if key_name not in raw_cfg:
            raise ValueError(f"{key_name} not found in config")

    def get_path(self, raw_cfg) -> Path:
        """verify raw_cfg["path"]"""
        self.verify_key_existance("path", raw_cfg)
        path = raw_cfg["path"]
        validate_path(path)
        return path

    def get_sheet(self, raw_cfg) -> str:
        """verify raw_cfg["sheet"]"""
        self.verify_key_existance("sheet", raw_cfg)
        sheet = raw_cfg["sheet"]
        validate_str(sheet, allow_zero=ALLOW_ZERO_STR)
        return sheet

    def get_header(self, raw_cfg) -> int:
        """verify raw_cfg["header"]"""
        self.verify_key_existance("header", raw_cfg)
        header = raw_cfg["header"]
        validate_positive_int(header)
        return header

    def get_register_as(self, raw_cfg) -> str:
        """
        verify raw_cfg["register_as"]

        add double quotes if it start with a number, 
        allow only alpha, numeric, underscore, and double quote characters
        """
        import re

        self.verify_key_existance("register_as", raw_cfg)
        raw_register_as = raw_cfg["register_as"]
        validate_str(raw_register_as, allow_zero=ALLOW_ZERO_STR)

        pattern = r"[^a-zA-Z0-9_\"]"

        register_as = re.sub(pattern, "_", raw_register_as.strip())
        
        if register_as[0].isdecimal():
            register_as = "\"" + register_as + "\""

        if register_as != raw_register_as:
            # TODO: log the change!
            pass

        return register_as

    @staticmethod
    def _normalize_kind(s: str):
        if s[0] == ".":
            s = s[1:]
        return s.lower().strip()

    def get_kind(self, raw_cfg):
        self.verify_key_existance("kind", raw_cfg)
        kind = raw_cfg["kind"]
        validate_str(kind, allow_zero=ALLOW_ZERO_STR)
        kind = self._normalize_kind(kind)
        if kind not in self.registry:
            raise KeyError(
                f"invalid kind: got {kind}. "
                "Options: ConfigNormalizer.registry"
            )
        return kind

    def _process_xl_cfg(self, raw_cfg) -> Mapping[str, str | int | Path]:
        path = self.get_path(raw_cfg)
        header = self.get_header(raw_cfg)
        register_as = self.get_register_as(raw_cfg)

        return {
            "path": path,
            "header": header,
            "register_as": register_as
        }

    def _process_csv_cfg(self, raw_cfg) -> Mapping[str, str | int | Path]:
        path = self.get_path(raw_cfg)
        header = self.get_header(raw_cfg)
        sheet = self.get_sheet(raw_cfg)
        register_as = self.get_register_as(raw_cfg)

        return {
            "path": path,
            "header": header,
            "sheet": sheet,
            "register_as": register_as
        }

    def from_cfg(
        self, 
        raw_cfg: Mapping[str, str | int]
    ):
        """
        pipeline entry, dispatch for frame types
        """
        kind = self.get_kind(raw_cfg)
        pipeline = self.registry[kind]
        cfg = pipeline(raw_cfg)
        cfg["kind"] = kind
        return cfg
        





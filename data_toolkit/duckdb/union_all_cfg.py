from dataclasses import dataclass
from typing import Sequence
import logging
from data_toolkit.duckdb.client import SQLCol

@dataclass(frozen=True)
class UnionAllCfg:
    name: str
    schema: list[SQLCol]
    branches: list[str]

    def __post_init__(self):
        
        self._validate_schema(self.schema)

        if " " in self.name:
            no_white_space = self.name.replace(" ", "")
            logging.info(f"{self.name} changed to {no_white_space}")
            object.__setattr__(self, "name", no_white_space)

    @staticmethod
    def _validate_schema(schema: Sequence[SQLCol]) -> None:
        for col in schema:
            if not isinstance(col, SQLCol):
                raise TypeError(
                    f"All columns in schema must be type Col. "
                    f"from data_toolkit.duckdb.execute"
                    )
from dataclasses import dataclass
import pandas as pd
from enum import Enum


class DateFmt(Enum):
    YYYY_MM_DD = '%Y-%m-%d' # yyyy-mm-dd

class DType(Enum):
    STR = "string"
    INT = "int"

class ColError(Enum):
    COERCE = "coerce"
    RAISE = "raise"

@dataclass(frozen=True)
class BaseCol:
    name: str

@dataclass(frozen=True)
class StrCol(BaseCol):
    pass

@dataclass(frozen=True)
class IntCol(BaseCol):
    errors: ColError

@dataclass(frozen=True)
class DateCol(BaseCol):
    format: DateFmt
    errors = ColError

COLUMNS = (BaseCol, StrCol, IntCol, DateCol)

def enforce_schema(
        schema: list[StrCol | DateCol | IntCol],
        df: pd.DataFrame
    ) -> pd.DataFrame:

    existing_columns = tuple(list(df.columns))

    for col in schema:

        if type(col) not in COLUMNS:
            raise TypeError(f"Invalid column class in schema")

        if col.name not in existing_columns:
            raise ValueError(f"{col.name} not found in dataframe")
        
        if isinstance(col, IntCol):
            df[col.name] = pd.to_numeric(df[col.name], errors=col.errors.value)

        elif isinstance(col, StrCol):
            df[col.name] = df[col.name].astype("string").str.strip()

        elif isinstance(col, DateCol):
            df[col.name] = pd.to_datetime(df[col.name], errors=col.errors, format=col.format.value)      

    return df





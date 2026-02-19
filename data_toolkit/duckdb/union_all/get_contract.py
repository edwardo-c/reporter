import importlib
from utils.validators import validate_str
from data_toolkit.duckdb.union_all.contract_projection import Col
from typing import Sequence

def _validate_schema(schema: Sequence[Col]) -> None:
    for col in schema:
        if not isinstance(col, Col):
            raise TypeError(
                f"All columns in schema must be type Col. "
                f"from data_toolkit.duckdb.contract_projection"
                )

def get_final_schema(module_name: str, final_schema_name: str = "FINAL_SCHEMA"): 
    
    validate_str(module_name, allow_zero=False)

    module = importlib.import_module(module_name, "union_all")
    
    if hasattr(module, final_schema_name):
        schema = getattr(module, final_schema_name)
    else:
        raise AttributeError(f"{final_schema_name} not found in {module}")

    _validate_schema(schema)

    return schema
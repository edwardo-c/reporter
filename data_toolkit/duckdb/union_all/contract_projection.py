import duckdb
from dataclasses import dataclass
from typing import Mapping

from data_toolkit.duckdb.union_all.cfg_validator import validate_cfg

from utils.validators import validate_str
from typing import Sequence
import importlib


@dataclass(frozen=True)
class Col():
    name: str
    dtype: str
    default_sql:str = "NULL"

def _validate_schema(schema: Sequence[Col]) -> None:
    for col in schema:
        if not isinstance(col, Col):
            raise TypeError(
                f"All columns in schema must be type Col. "
                f"from data_toolkit.duckdb.contract_projection"
                )

def get_final_schema(
        module_name: str, 
        final_schema_name: str = "FINAL_SCHEMA"
    ): 
    
    validate_str(module_name, allow_zero=False)

    module = importlib.import_module(module_name)
    
    if hasattr(module, final_schema_name):
        schema = getattr(module, final_schema_name)
    else:
        raise AttributeError(f"{final_schema_name} not found in {module}")

    return schema


def get_columns(conn: duckdb.DuckDBPyConnection, relation: str) -> tuple[str]:
    result = conn.execute(f"DESCRIBE {relation}").fetchall()
    return tuple(r[0] for r in result)

def create_projection_query(
        existing_columns: tuple[str], 
        relation: str, 
        schema: list[Col]) -> str:
    """produces a single sql SELECT statement with a CanonicalSchema enforced"""
    exprs = []
    for col in schema:
        if col.name in existing_columns:
            exprs.append(f'CAST("{col.name}" AS {col.dtype}) AS "{col.name}"')
        else:
            exprs.append(f'CAST({col.default_sql} AS {col.dtype}) AS "{col.name}"')
    
    return "SELECT\n " + ", \n".join(exprs) + f"\nFROM {relation}"

def materialize_intermediate_view(
        conn: duckdb.DuckDBPyConnection,
        projection_name: str,
        projection_sql:str
    ) -> str:
    """
    expects projection_sql to be a complete SELECT statement
    
    projection_sql example:
    
      SELECT a, b FROM tbl
    """
    assert projection_sql.lstrip().lower().startswith("select"), (
        f"projection_sql must be a complete SELECT statement; got: {projection_sql}"
    )
    conn.execute(f"CREATE OR REPLACE TEMP VIEW _{projection_name} AS {projection_sql}")
    return f"_{projection_name}"

def create_union_all_query(views: list[str]):
    """generates union all statement for list of view names"""
    expr = [f"SELECT * FROM {view}" for view in views]
    return "\nUNION ALL\n".join(expr)

def execute_union_all(
        conn: duckdb.DuckDBPyConnection,
        *, 
        final_name: str,
        union_all_projection_sql,
        
    ):
    sql = f"CREATE OR REPLACE TEMP VIEW {final_name} AS {union_all_projection_sql}"
    conn.execute(sql)

# ======================== ENTRY ============================
def contract_enforced_union_all(
        raw_cfg: Mapping[str, str | list[str]],
        conn: duckdb.DuckDBPyConnection
    ) -> str:
    """
    Materializes union all view of branches
    returns name of final union all from raw_cfg
    Raises invalid config
    """
    # validate config
    validate_cfg(raw_cfg)
    final_view_cfg = raw_cfg["final_view"]
    schema_cfg = raw_cfg["schema"]
    branches_cfg = raw_cfg["branches"]

    final_schema = get_final_schema(**schema_cfg)
    _validate_schema(final_schema)

    intermediate_views_exprs = []

    for branch in branches_cfg:
        # enforce contract for each branch
        """
        create select all statement in the order of the provided schema
        """
        existing_columns = get_columns(conn, branch)
        projection_sql = create_projection_query(existing_columns, branch, final_schema)
        
        intermediate_view = materialize_intermediate_view(conn, branch, projection_sql)

        intermediate_views_exprs.append(intermediate_view)

    union_all_query = create_union_all_query(intermediate_views_exprs)

    execute_union_all(
        conn, 
        final_name=final_view_cfg["name"], 
        union_all_projection_sql=union_all_query
    )

    return final_view_cfg["name"]





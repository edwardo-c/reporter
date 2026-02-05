import duckdb
from dataclasses import dataclass

@dataclass(frozen=True)
class Col():
    name: str
    dtype: str
    default_sql:str = "NULL"

@dataclass(frozen=True)
class RelationPair():
    """
    logic: name of existing sql logic view
    final: name of CanonicalSchema enforced view
    """
    logic: str
    final: str

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

def materialize_view(
        conn: duckdb.DuckDBPyConnection,
        final_view_name: str,
        projection_sql:str
    ):
    """
    expects projection_sql to be a complete SELECT statement
    
    projection_sql example:
    
      SELECT a, b FROM tbl
    """
    assert projection_sql.lstrip().lower().startswith("select"), (
        f"projection_sql must be a complete SELECT statement; got: {projection_sql}"
    )
    conn.execute(f"CREATE OR REPLACE TEMP VIEW {final_view_name} AS {projection_sql}")
    return final_view_name

def create_union_all_query(views: list[str]):
    """generates union all statement for list of view names"""
    expr = [f"SELECT * FROM {view}" for view in views]
    return "\nUNION ALL\n".join(expr)

def contract_enforced_union_all(
        conn: duckdb.DuckDBPyConnection, 
        schema: list[Col],
        relation_pairs: list[RelationPair],
        final_view_name: str = "temp_stg_view",
    ):

    for pair in relation_pairs:

        existing_columns = get_columns(conn, pair.logic)

        projection_sql = create_projection_query(existing_columns, pair.logic, schema)

        materialize_view(conn, pair.final, projection_sql)

    final_views = [pair.final for pair in relation_pairs]
    union_all_query = create_union_all_query(final_views)

    materialize_view(conn, final_view_name, union_all_query)

    return final_view_name

# All pair.final views must share identical column order + types (enforced by schema projection).
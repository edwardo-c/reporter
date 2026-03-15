# import duckdb
# from dataclasses import dataclass
# from typing import Sequence
# import logging

# @dataclass(frozen=True)
# class Col():
#     name: str
#     dtype: str
#     default_sql:str = "NULL"

# @dataclass(frozen=True)
# class UnionAllCfg:
#     name: str
#     schema: list[Col]
#     branches: list[str]

#     def __post_init__(self):
        
#         self._validate_schema(self.schema)

#         if " " in self.name:
#             no_white_space = self.name.replace(" ", "")
#             logging.info(f"{self.name} changed to {no_white_space}")
#             object.__setattr__(self, "name", no_white_space)

#     @staticmethod
#     def _validate_schema(schema: Sequence[Col]) -> None:
#         for col in schema:
#             if not isinstance(col, Col):
#                 raise TypeError(
#                     f"All columns in schema must be type Col. "
#                     f"from data_toolkit.duckdb.execute"
#                     )

# def get_columns(conn: duckdb.DuckDBPyConnection, relation: str) -> tuple[str]:
#     result = conn.execute(f"DESCRIBE {relation}").fetchall()
#     return tuple(r[0] for r in result)

# def create_projection_query(
#         existing_columns: tuple[str], 
#         relation: str, 
#         schema: list[Col],
#     ) -> str:
#     """produces a single sql SELECT statement with a CanonicalSchema enforced"""
#     exprs = []
#     for col in schema:
#         if col.name in existing_columns:
#             exprs.append(f'CAST("{col.name}" AS {col.dtype}) AS "{col.name}"')
#         else:
#             exprs.append(f'CAST({col.default_sql} AS {col.dtype}) AS "{col.name}"')
    
#     return "SELECT\n " + ", \n".join(exprs) + f"\nFROM {relation}"

# def materialize_intermediate_view(
#         conn: duckdb.DuckDBPyConnection,
#         projection_name: str,
#         projection_sql:str
#     ) -> str:
#     """
#     expects projection_sql to be a complete SELECT statement
    
#     projection_sql example:
    
#       SELECT a, b FROM tbl
#     """
#     assert projection_sql.lstrip().lower().startswith("select"), (
#         f"projection_sql must be a complete SELECT statement; got: {projection_sql}"
#     )
#     conn.execute(f"CREATE OR REPLACE TEMP VIEW _{projection_name} AS {projection_sql}")
#     return f"_{projection_name}"

# def create_union_all_query(views: list[str]):
#     """generates union all statement for list of view names"""
#     expr = [f"SELECT * FROM {view}" for view in views]
#     return "\nUNION ALL\n".join(expr)

# def execute_union_all(
#         conn: duckdb.DuckDBPyConnection,
#         *, 
#         final_name: str,
#         union_all_projection_sql,
        
#     ):
#     sql = f"CREATE OR REPLACE TEMP VIEW {final_name} AS {union_all_projection_sql}"
#     conn.execute(sql)

# # ======================== ENTRY ============================
# def contract_enforced_union_all(
#         cfg: UnionAllCfg,
#         conn: duckdb.DuckDBPyConnection
#     ) -> None:
#     """
#     Materializes union all view of branches
#     Raises invalid config
#     """

#     if not isinstance(cfg, UnionAllCfg):
#         raise TypeError(f"invalid cfg, expected ..UnionAllCfg, got: {type(cfg).__name__}")

#     intermediate_views_exprs = []

#     for branch in cfg.branches:
#         # enforce contract for each branch
#         """
#         create select all statement in the order of the provided schema
#         """
#         existing_columns = get_columns(conn, branch)
#         projection_sql = create_projection_query(
#             existing_columns, 
#             branch, 
#             cfg.schema
#         )
        
#         intermediate_view = materialize_intermediate_view(conn, branch, projection_sql)

#         intermediate_views_exprs.append(intermediate_view)

#     union_all_query = create_union_all_query(intermediate_views_exprs)

#     execute_union_all(
#         conn, 
#         final_name=cfg.name, 
#         union_all_projection_sql=union_all_query
#     )





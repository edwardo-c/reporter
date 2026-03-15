import duckdb
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class SQLCol():
    name: str
    dtype: str
    default_sql:str = "NULL"

class DuckRunner:
    def __init__(self, db_path: Path | str | None):
        self.db_path = db_path

    def __enter__(self):
        self.conn = (
            duckdb.connect(self.db_path) 
            if self.db_path 
            else duckdb.connect()
        )
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn: self.conn.close()

    def run_sql_file(self, file_path: Path) -> None:
        sql = file_path.read_text(encoding="utf-8")
        self.conn.execute(sql)

    def run_ordered_sql(self, file_paths: list[Path]) -> None:
        for f in file_paths:
            self.run_sql_file(f)

    # ======================= CONTRACT ENFORCED UNION ALL =============================

    def _execute_union_all(
            self,
            *, 
            final_name: str,
            union_all_projection_sql,    
        ) -> None:
        sql = f"CREATE OR REPLACE TEMP VIEW {final_name} AS {union_all_projection_sql}"
        self.conn.execute(sql)

    def _materialize_intermediate_view(
            self,
            projection_name: str,
            projection_sql:str
        ) -> str:
        """
        expects projection_sql to be a complete SELECT statement

        projection_sql example: SELECT a, b FROM tbl
        """
        assert projection_sql.lstrip().lower().startswith("select"), (
            f"projection_sql must be a complete SELECT statement; got: {projection_sql}"
        )

        self.conn.execute(f"CREATE OR REPLACE TEMP VIEW _{projection_name} AS {projection_sql}")
        return f"_{projection_name}"
    
    @staticmethod
    def _create_union_all_query(views: list[str]):
        """generates union all statement for list of view names"""
        expr = [f"SELECT * FROM {view}" for view in views]
        return "\nUNION ALL\n".join(expr)

    def _create_projection_query(
                self,
                existing_columns: tuple[str], 
                relation: str, 
                schema: list[SQLCol],
            ) -> str:
            """produces a single sql SELECT statement with a CanonicalSchema enforced"""
            exprs = []
            for col in schema:
                if col.name in existing_columns:
                    exprs.append(f'CAST("{col.name}" AS {col.dtype}) AS "{col.name}"')
                else:
                    exprs.append(f'CAST({col.default_sql} AS {col.dtype}) AS "{col.name}"')
            
            return "SELECT\n " + ", \n".join(exprs) + f"\nFROM {relation}"

    def get_columns(self, relation: str) -> tuple[str]:
            result = self.conn.execute(f"DESCRIBE {relation}").fetchall()
            return tuple(r[0] for r in result)

    def contract_enforced_union_all(
            self,
            final_name: str,
            branches: list[str],
            schema: list[SQLCol]
        ) -> None:

        intermediate_views = []

        for branch in branches:
            # enforce contract for each branch
            """
            create select all statement in the order of the provided schema
            """
            projection_sql = self._create_projection_query(
                self.get_columns(branch), 
                branch, 
                schema
            )
            
            intermediate_view = self._materialize_intermediate_view(branch, projection_sql)

            intermediate_views.append(intermediate_view)

        union_all_query = self._create_union_all_query(intermediate_views)

        self._execute_union_all(final_name=final_name, union_all_projection_sql=union_all_query)
from dataclasses import dataclass
import duckdb
import importlib

@dataclass(frozen=True)
class Col:
    name: str
    dtype: str
    default_sql: str = "NULL"

# ======== Create Contract View for a relation ==============

def relation_columns(con: duckdb.DuckDBPyConnection, relation: str) -> set[str]:
    rows = con.execute(f"DESCRIBE SELECT * FROM {relation}").fetchall()
    return {r[0] for r in rows}

def build_contract_projection_sql(
    relation: str,
    schema: list[Col],
    available_cols: set[str],
    mode: str = "defaults",  # "defaults" or "strict"
) -> str:
    exprs = []
    missing = []
    for col in schema:
        if col.name in available_cols:
            exprs.append(f'CAST("{col.name}" AS {col.dtype}) AS "{col.name}"')
        else:
            if mode == "strict":
                raise ValueError(f"Missing required column {col.name} in {relation}")
            exprs.append(f'CAST({col.default_sql} AS {col.dtype}) AS "{col.name}"')

    return "SELECT\n  " + ",\n  ".join(exprs) + f"\nFROM {relation}"

def create_contract_view(
    con: duckdb.DuckDBPyConnection,
    logic_view: str,
    final_view: str,
    schema: list[Col],
    mode: str = "defaults",
) -> None:
    cols = relation_columns(con, logic_view)
    select_sql = build_contract_projection_sql(logic_view, schema, cols, mode=mode)
    con.execute(f"CREATE OR REPLACE TEMP VIEW {final_view} AS\n{select_sql}")

#  ====== Generate UNION ALL View for multiple Contract-enforced Relations ===============
def create_union_view(
    con: duckdb.DuckDBPyConnection,
    union_view: str,
    final_views: list[str],
) -> None:
    union_sql = "\nUNION ALL\n".join([f"SELECT * FROM {v}" for v in final_views])
    con.execute(f"CREATE OR REPLACE TEMP VIEW {union_view} AS\n{union_sql}")

def load_schema_from_module(module_name: str):
    mod = importlib.import_module(module_name)
    return mod.FINAL_SCHEMA  # list[Col]

# ========== ENTRY ==========
def run_finalize(con, finalize_cfg):
    schema = load_schema_from_module(finalize_cfg["contract"]["schema_module"])
    mode = finalize_cfg["contract"].get("mode", "defaults")

    for union in finalize_cfg["unions"]:
        union_name = union["name"]
        branches = union["branches"]

        final_views = []
        for b in branches:
            create_contract_view(
                con=con,
                logic_view=b["logic_view"],
                final_view=b["final_view"],
                schema=schema,
                mode=mode
            )
            final_views.append(b["final_view"])

        create_union_view(con, union_name, final_views)

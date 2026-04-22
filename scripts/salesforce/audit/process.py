"""loads data from outside sources"""
from data_toolkit.readers.readers import get_dataframe_from_source
from data_toolkit.readers.context import ReaderContext
import duckdb
from data_toolkit.readers.sources import SFQuery, OData
from scripts.salesforce.audit.jobs_registry import AuditObj, get_job
from data_toolkit.duckdb.client import execule_sql_path
import pandas as pd

def _conn() -> duckdb.DuckDBPyConnection:
    """
    returns fresh connection for clean sql workspace
    """
    return duckdb.connect()

def load_data(
        sources: list[SFQuery | OData], 
        context: ReaderContext,
        conn: duckdb.DuckDBPyConnection
    ) -> None:
    """dispatch for loading data from sources into db to enable sql"""
    for s in sources:
        df = get_dataframe_from_source(s, context)
        conn.register(s.df_id, df)

def run_jobs(
        jobs_cfg: dict[str, bool],
        ctx: ReaderContext
    ) -> None:
    """runs all jobs from provided jobs_cfg with fresh duckdb connection per job"""
    for k, v in jobs_cfg.items():
        if v: 
            job_cfg: AuditObj | None = get_job(k)
        
            conn = _conn()
        
            load_data(job_cfg.sources, context=ctx, conn=conn)

            execule_sql_path(sql_path=job_cfg.sql, conn=conn)

            # testing block ==========
            df: pd.DataFrame = conn.execute(f"SELECT * FROM duplicates_in_sf").df()
            breakpoint()
            # testing end ============

            # df: pd.DataFrame = conn.execute(f"SELECT * FROM {job_cfg.final_name}").df()

            # df.to_csv(job_cfg.out_path, index=False)

"""loads data from outside sources"""
from data_toolkit.readers.readers import get_dataframe_from_source
from data_toolkit.readers.context import ReaderContext
import duckdb
from data_toolkit.readers.sources import SFQuery, OData

def query_and_load(
        sources: list[SFQuery | OData], 
        context: ReaderContext,
        conn: duckdb.DuckDBPyConnection
    ) -> None:
    """dispatch for loading data from sources into db to enable sql"""
    for s in sources:
        df = get_dataframe_from_source(s, context)
        conn.register(s.df_id, df)
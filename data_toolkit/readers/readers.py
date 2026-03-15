from data_toolkit.readers.registry import READERS_REGISTRY
from data_toolkit.readers.sources import XLBundle, CSV, DispatchEnum, SFQuery
from data_toolkit.readers.registry import register_reader
import pandas as pd
from data_toolkit.readers.context import ReaderContext

def get_dataframe_from_source(
        src, 
        context: ReaderContext | None = None
    ) -> dict[str, pd.DataFrame] | pd.DataFrame:
    reader_func = READERS_REGISTRY[src.src_type]
    data = reader_func(src, context=context)
    return data

@register_reader(DispatchEnum.BUNDLE.value)
def read_xlbundle(src: XLBundle, context: ReaderContext | None = None) -> dict[str, pd.DataFrame]:
    result = {}
    io = str(src.path)
    for part in src.parts:
        result[part.df_id] = pd.read_excel(
            io=io,
            sheet_name=part.sheet_name,
            header=part.header
        )
    return result

@register_reader(DispatchEnum.CSV.value)
def read_csv(src: CSV, context: ReaderContext | None = None) -> pd.DataFrame:
    return pd.read_csv(
        filepath_or_buffer=str(src.path),
        header=src.header
        )

@register_reader(DispatchEnum.SF.value)
def sf_query_all(src: SFQuery, context: ReaderContext | None) -> pd.DataFrame:
    if context is None or context.sf is None:
        raise ValueError("Salesforce connection is required for SFQuery sources.")
    
    res = context.sf.query_all(src.soql)
    records = res["records"]
    return pd.DataFrame(records).drop(columns=["attributes"], errors="ignore")
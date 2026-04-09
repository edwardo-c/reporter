"""useful if reading multiple dataframes in a single system"""

from data_toolkit.readers.registry import READERS_REGISTRY
from data_toolkit.readers.sources import XLBundle, CSV, DispatchEnum, SFQuery, OData
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
def read_sf_query(src: SFQuery, context: ReaderContext | None) -> pd.DataFrame:
    if context is None or context.sf is None:
        raise ValueError("Salesforce connection is required for SFQuery sources.")
    
    res = context.sf.query_all(src.soql)
    records = res["records"]

    df = pd.json_normalize(records, sep=".")
    return df.drop(columns=["attributes"], errors="ignore")

@register_reader(DispatchEnum.ODATA.value)
def read_odata(src: OData, context: ReaderContext | None):
    if context is None or context.acu is None:
        raise ValueError("requests.Session() is required for OData sources.")
    
    res = context.acu.get(src.url, params=src.params)

    try:
        payload: dict = res.json()
    except ValueError:
        raise ValueError(f"Non-JSON response from Acumatica: {res.text[:200]}")

    data = payload.get("value", [])

    if not data:
        raise ValueError(f"Odata url returned nothing! -- {src.url}")

    return pd.json_normalize(data)
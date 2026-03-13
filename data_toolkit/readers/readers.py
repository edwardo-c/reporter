from data_toolkit.readers.registry import READERS_REGISTRY
from data_toolkit.readers.sources import XLBundle, Sources
from data_toolkit.readers.registry import register_reader
import pandas as pd

def get_dataframe_from_source(src: XLBundle) -> dict[str, pd.DataFrame] | pd.DataFrame:
    reader_func = READERS_REGISTRY[src.src_type]
    data = reader_func(src)
    return data

@register_reader(Sources.BUNDLE.value)
def read_xlbundle(bundle: XLBundle) -> dict[str, pd.DataFrame]:
    result = {}
    io = str(bundle.path)
    for part in bundle.parts:
        result[part.part_id] = pd.read_excel(
            io=io,
            sheet_name=part.sheet_name,
            header=part.header
        )
    return result







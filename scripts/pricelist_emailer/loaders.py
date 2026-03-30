import pandas as pd
from data_toolkit.readers.readers import sf_query_all
from data_toolkit.readers.context import ReaderContext
from scripts.pricelist_emailer.config import PriceListSFQueries
from data_toolkit.cleaners.df_dtypes.dtype import enforce_schema
from dataclasses import dataclass

@dataclass(frozen=True)
class PriceListDFContactsFrames:
    external: pd.DataFrame
    internal: pd.DataFrame

def load_contacts(
        queries: PriceListSFQueries, 
        context: ReaderContext
    ) -> PriceListDFContactsFrames:

    external_df = sf_query_all(queries.external.query, context=context)
    internal_df = sf_query_all(queries.internal.query, context=context)

    # validate schema and clean
    external_df = enforce_schema(queries.external.schema, external_df)
    internal_df = enforce_schema(queries.internal.schema, internal_df)

    return PriceListDFContactsFrames(
        external=external_df,
        internal=internal_df
    )
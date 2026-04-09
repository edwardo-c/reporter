import pandas as pd

from data_toolkit.cleaners.schema import enforce_schema
from data_toolkit.readers.context import ReaderContext
from data_toolkit.readers.readers import get_dataframe_from_source
from data_toolkit.readers.sources import OData
from scripts.pricelist.emailer.config import PriceListQuery

def _load_df(
        query_obj: PriceListQuery, 
        context: ReaderContext
    ) -> pd.DataFrame:

    df = get_dataframe_from_source(query_obj.query, context)
    
    df = enforce_schema(query_obj.schema, df)[[c.name for c in query_obj.schema]]

    df = df.rename(columns=query_obj.rename_map)

    return df.drop_duplicates()

def load_contacts_df(
        internal_query: PriceListQuery,
        external_query: PriceListQuery,
        context: ReaderContext
    ) -> pd.DataFrame:
    """"
    compiles internal and external query into a single dataframe
    """
    
    internal_df = _load_df(internal_query, context)
    external_df = _load_df(external_query, context)
    stacked = pd.concat([internal_df, external_df])

    if len(stacked) == 0:
        raise ValueError(
            f"contact_map is empty!\n"
            f"Did SOQL queries return data?"
        )

    return stacked

def load_customers_df(
        customers_odata_obj: OData,
        context: ReaderContext
    ) -> pd.DataFrame:

    df = _load_df(customers_odata_obj, context)

    return df



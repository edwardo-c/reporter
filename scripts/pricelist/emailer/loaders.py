# querying data from external sources
import pandas as pd

from data_toolkit.cleaners.schema import enforce_schema
from data_toolkit.readers.context import ReaderContext
from data_toolkit.readers.readers import get_dataframe_from_source
from scripts.pricelist.emailer.config import PriceListQuery
from scripts.pricelist.emailer.config import Sources

from dataclasses import dataclass

@dataclass
class ExternalData:
    contacts: pd.DataFrame
    customers: pd.DataFrame

def process_df(query_obj: PriceListQuery, df: pd.DataFrame) -> pd.DataFrame:
    """
    clean and truncate dataframe

    uses .schema and .rename_map from query obj
    """
    _df = df.copy()
    _df = enforce_schema(query_obj.schema, _df)[[c.name for c in query_obj.schema]]
    _df = _df.rename(columns=query_obj.rename_map)
    return _df.drop_duplicates()

def load_contacts_df(
        internal_query: PriceListQuery,
        external_query: PriceListQuery,
        context: ReaderContext
    ) -> pd.DataFrame:
    """"
    compiles internal and external query into a single dataframe
    """
    
    internal_df = get_dataframe_from_source(internal_query.query, context)
    internal_df = process_df(internal_query, internal_df)
    
    external_df = get_dataframe_from_source(external_query.query, context)
    external_df = process_df(external_query, external_df)

    stacked = pd.concat([internal_df, external_df])

    if len(stacked) == 0:
        raise ValueError(
            f"contact_map is empty!\n"
            f"Did SOQL queries return data?"
        )

    return stacked

def load_customers(query_obj: PriceListQuery, ctx: ReaderContext):
    df = get_dataframe_from_source(query_obj.query, ctx)
    df = process_df(query_obj, df)
    return df

def get_external_data(
        srcs: Sources,
        ctx: ReaderContext
    ) -> ExternalData:
    """
    Primary runner to query all external data sources
    """
    return ExternalData(
        contacts=load_contacts_df(
            srcs.sf_internal_query, 
            srcs.sf_external_query, 
            ctx
        ), 
        customers=load_customers(
            srcs.acu_customers_query,
            ctx
        )
    )


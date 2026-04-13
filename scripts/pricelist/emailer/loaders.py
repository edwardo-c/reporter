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

def process_df(query_obj: PriceListQuery) -> pd.DataFrame:
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
    
    internal_df = get_dataframe_from_source(internal_query, context)
    internal_df = process_df(internal_query)
    
    external_df = get_dataframe_from_source(external_query, context)
    external_df = process_df(external_query)

    stacked = pd.concat([internal_df, external_df])

    if len(stacked) == 0:
        raise ValueError(
            f"contact_map is empty!\n"
            f"Did SOQL queries return data?"
        )

    return stacked

def get_external_data(
        srcs: Sources,
        ctx: ReaderContext
    ) -> ExternalData:
    """
    Primary runner to query all external data sources
    
    Returns ExternalData object with queried dataframes
    """

    """
    pattern is load process, but for contacts, you also stack
    """

    return ExternalData(
        contacts=load_contacts_df(
            srcs.sf_internal_query.query, 
            srcs.sf_external_query.query, 
            ctx
        ), 
        
        customers=process_df(
            get_dataframe_from_source(srcs.acu_customers_query.query, ctx)
        )

    )


import pandas as pd
import numpy as np
from decimal import Decimal

# useful but created by AI, will need to study this

def serialize_dataframe_for_api(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert dataframe values into JSON-safe primitives for API transport.
    """
    
    df = df.copy()

    for col in df.columns:

        # Convert datetime columns to ISO string
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime("%Y-%m-%d")

        # Convert numpy numbers to Python numbers
        elif pd.api.types.is_integer_dtype(df[col]):
            df[col] = df[col].astype("Int64").astype(object)

        elif pd.api.types.is_float_dtype(df[col]):
            df[col] = df[col].astype(float)

    # Replace NaN with None
    df = df.replace({np.nan: None})

    # Convert Decimal if present
    df = df.map(lambda x: float(x) if isinstance(x, Decimal) else x)

    return df
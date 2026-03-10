"""
prepare wide for bulk upsert

expected shape: 
    list of dictionaries where each dictionary is a row
    prefer df.to_dict('records')
        
"""
import pandas as pd

from dataclasses import dataclass

@dataclass(frozen=True)
class ExternalID:
    name: str
    id_parts: tuple[str, ...]

def df_bulk_payload(
        df: pd.DataFrame, 
        external_id: ExternalID
    ) -> dict:

    existing_cols = list(df.columns)
    for part in external_id.id_parts:
        if part not in existing_cols:
            raise ValueError(f"{part} column does not exist in dataframe")

    # create composite External ID Key
    df[external_id.name] = df[external_id.id_parts].astype(str).agg('|'.join, axis=1)

    payload = df.to_dict('records')
    
    return payload
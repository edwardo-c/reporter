"""
prepare wide for bulk upsert

expected shape: 
    list of dictionaries where each dictionary is a row
    prefer df.to_dict('records')
        
"""
import pandas as pd

from dataclasses import dataclass

@dataclass(frozen=True)
class BulkObj:
    name: str
    external_id_name: str
    external_id_parts: tuple[str, ...]


def valid_payload(
        payload: list[dict],
        bulk_obj: BulkObj
    ) -> bool:

    if not isinstance(payload, list):
            raise TypeError(
                f"Invalid payload, expected list[dict], got: {type(payload).__name__}"
            )

    for p in payload:
        
        if not isinstance(p, dict):
            raise TypeError(
                f"Expected payload shape list[dict]\n"
                f"found type {type(p).__name__} in payload"
                )

        if bulk_obj.external_id_name not in p:
            raise KeyError(
                f"dict without {bulk_obj.external_id_name} found.\n"
                f"Each dict must contain {bulk_obj.external_id_name}"
            )

        ex_id = p[bulk_obj.external_id_name]

        if ex_id == None or ex_id == "":
            raise ValueError(
                f"External ID's cannot be None or Blank"
            )
    
    return True

def build_bulk_payload(
        df: pd.DataFrame, 
        bulk_obj: BulkObj,
        validate: bool = True
    ) -> dict:
    """
    Build Salesforce bulk API payload from a dataframe that already
    conforms to the final schema contract.
    Assumes required columns and NOT NULL constraints are enforced upstream.
    """
    _df = df.copy()

    _df[bulk_obj.name] = _df[bulk_obj.external_id_parts].astype(str).agg('|'.join, axis=1)

    payload = _df.to_dict('records')
    
    if validate: valid_payload(payload, bulk_obj)

    return payload
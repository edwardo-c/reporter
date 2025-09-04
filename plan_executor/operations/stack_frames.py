"""Append multiple Dataframes into a single"""
import logging

import pandas as pd

from plan_executor.registry import register_operation

logger = logging.getLogger(__name__)

@register_operation("stack_frames")
def stack_frames(data: list[dict[str, pd.DataFrame]], *,
                 schema: list[str], source: bool = True):
    """Append dataframes into a single stacked dataframe"""
    
    if not isinstance(data, list):
        raise TypeError(f"expected type list, received {type(data)}")

    if not isinstance(schema, list):
        raise ValueError(f"schema required, recieved none")

    # log missing fields
    _missing_fields(data=data, schema=schema)
    
    data_sets = []

    for d in data:
        # expected [{"alias": "data_1", "data": pd.DataFrame},]
        dfx, alias = d.get("data", pd.DataFrame()).copy(), d.get("alias", "no_alias_found")
  
        if dfx.empty:
            logger.warning("empty data frame detected for alias: %s!", alias)

        # TODO: accept explicitly handle no alias

        if source:
            cols = [c for c in schema if c != "source"] + ["source"] 
            dfx["source"] = alias
        else:
            cols = [c for c in schema if c]

        dfx = dfx.reindex(columns=cols, fill_value=pd.NA) 
     
        data_sets.append(dfx)

    # output result in given schema order
    return pd.concat(data_sets, ignore_index=True)


def _missing_fields(data: list[dict[str, pd.DataFrame]], 
                    schema: list[str]) -> dict[str, list]:
    """Check all dataframes for schema, return missing fields"""
    missing = []
    for d in data:
        if not isinstance(d, dict):
            raise ValueError(
                f"expected type dict, recieved {type(d)}")
        
        alias = d.get("alias")
        data = d.get("data", pd.DataFrame())
        
        if data.empty:
            logger.info("no data found in alias: %s", alias)
        
        miss = [s for s in schema if s not in data.columns]
        if miss:
            missing.append({"alias": alias, "missing": miss})

    if missing:         
        logger.info("%s missing %s from schema", alias, missing)    

    return missing
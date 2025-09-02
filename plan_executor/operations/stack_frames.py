"""Append multiple Dataframes into a single"""
import logging

import pandas as pd

from plan_executor.registry import register_operation
from utils.logging_config import setup_logging

logger = logging.getLogger(__name__)

@register_operation("stack_frames")
def stack_frames(frames: dict[str, pd.DataFrame], 
                 schema: list[str], strict: bool = False):
    """Append dataframes into a single stacked dataframe"""
    
    # log missing fields
    missing = _missing_fields(frames=frames, schema=schema)
    if strict and missing:
        raise ValueError(
            f"missing from schema: {missing}\nschema: {schema}")

def _missing_fields(frames: list[dict[str, pd.DataFrame]], 
                    schema: list[str]) -> dict[str, list]:
    """Check all dataframes for schema, return missing fields"""
    missing = []
    for frame in frames:
        if not isinstance(frame, dict):
            raise ValueError(
                f"expected type dict, recieved {type(frame)}")
        
        alias = frame.get("alias")
        data = frame.get("data", pd.DataFrame({"empty":[]}))
        
        if data.empty:
            raise ValueError(
                f"missing data frame from alias: {alias}")
        
        m = [s for s in schema if s not in data.columns]
        if m:
            missing.append({"alias": alias, "missing": m})

    if missing:         
        logger.info("%s missing %s from schema", alias, missing)    

    return missing
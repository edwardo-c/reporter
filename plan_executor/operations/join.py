"""Pandas merge wrapped for use in .execute_steps()"""

import pandas as pd
import numpy as np

from plan_executor.registry import register_operation

@register_operation("join")
def join(
    df: pd.DataFrame, 
    *,
    right: pd.DataFrame,
    how: str,
    on: list[str]
    ):
    """
    Pandas merge operations
    accepts yaml dict as dataframe for right
    returns merged dataframe with right
    raises:
      invalid right data frame

    """
    if not isinstance(right, (dict, pd.DataFrame)):
      raise TypeError(
        f"'right' must be pd.Dataframe or convertable (dict[str, list]")
    
    if all(
        isinstance(k, str) and isinstance(v, list) 
        for k, v in right.items()
    ):
      try:
        right = pd.DataFrame(right)
      except Exception as e:
        raise TypeError(
          f"unable to convert right to dataframe: {right}, {e}")
  
    return df

        

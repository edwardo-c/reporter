import inspect
import logging

import pandas as pd
from plan_executor.registry import OPERATIONS_REGISTRY

logger = logging.getLogger(__name__)

def execute_steps(plan: list, df: pd.DataFrame | None = None):
    for step in plan:
        fn = OPERATIONS_REGISTRY[step["op"]]
        args = step.get("args", {}) or {}

        sig = inspect.signature(fn)
        params = set(sig.parameters)

        # pass df only if the op accepts it
        if "df" in params:
            result = fn(df=df, **args)
        else:
            result = fn(**args)

        if isinstance(result, pd.DataFrame):
            df = result
    return df

import inspect
import logging

import pandas as pd
from plan_executor.registry import OPERATIONS_REGISTRY

logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

def execute_steps(plan: list, data=None):
    for i, step in enumerate(plan, 1):
        fn = OPERATIONS_REGISTRY[step["op"]]
        args = step.get("args") or {}

        sig = inspect.signature(fn)
        params = sig.parameters

        if "df" in params:
            result = fn(df=data, **args)
        elif "data" in params:
            result = fn(data=data, **args)
        else:
            result = fn(**args)

        logger.debug("Step %s '%s' -> %s", i, step["op"], type(result).__name__)

        if result is not None:
            data = result
        else:
            logger.debug("Step %s returned None; keeping previous data.", i)

    return data
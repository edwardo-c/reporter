from typing import Dict

import pandas as pd

from plan_executor.registry import REGISTRY_TRANSFORMS
from plan_executor import registry

class DataPlanExecutor():
    def __init__(self, data: pd.DataFrame, data_plan: dict):
        self.data: pd.DataFrame = data
        self.data_plan: list[dict] = data_plan
        self.registry = REGISTRY_TRANSFORMS
        self.processed_data = self._apply_steps()

    def _apply_steps(self):
        df = self.data

        for step in self.data_plan:
            if not isinstance(step, dict):
                raise ValueError(f"expected type dict, recieved {type(step)}")

            op: str = step['op']
            args: Dict = step['args']
            func = self.registry[op]
            df = func(df, args)
        
        return df
        
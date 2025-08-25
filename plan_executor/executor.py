from typing import Dict

import pandas as pd

from plan_executor.registry import OPERATIONS_REGISTRY
from plan_executor import registry

def execute_steps(plan: dict):
    for step in plan:
        func = OPERATIONS_REGISTRY[step['op']]
        cfg = step['cfg']
        return func(cfg)

        
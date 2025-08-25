import pandas as pd
import inspect
from plan_executor.registry import OPERATIONS_REGISTRY

def execute_steps(plan: list, **context) -> pd.DataFrame:
    state = {"df": None, **context}

    for step in plan:
        fn = OPERATIONS_REGISTRY[step["op"]]
        args = step.get("args", {})

        # Build call kwargs: inject state keys only if the function accepts them
        sig = inspect.signature(fn)
        call = {k: v for k, v in state.items() if k in sig.parameters}
        # Step args (from YAML) always win
        if isinstance(args, dict):
            call.update(args)

        result = fn(**call)

        if isinstance(result, pd.DataFrame):
            state["df"] = result
        elif isinstance(result, dict):
            state.update(result)

    return state["df"]  # you expect a DataFrame back

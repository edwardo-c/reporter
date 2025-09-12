# standard library imports

# # Third party imports
# import pandas as pd

# # Internal Application Imports
# from config.paths import PRICE_LIST_YAML
# from utils.yaml_loader import load_yaml # also loads dotenv secrets
# from plan_executor.executor import execute_steps

# def main():
#     # load entire configuration for process
#     cfg = load_yaml(PRICE_LIST_YAML)
    
#     # import data
#     data_load_plan = cfg["load"]
#     df: pd.DataFrame = execute_steps(plan=data_load_plan)
    
#     # manipulate shade data frame
#     shade_data_plan = cfg["plans"]["shade"]
#     shade_data = execute_steps(shade_data_plan, df=df)

#     # manipulate non-shade data frame
#     non_shade_data_plan = cfg["plans"]["non_shade"]
#     non_shade_data = execute_steps(non_shade_data_plan, df=df)

#     # export shade data frames
#     shade_export_plan = cfg["exports"]["shade"]
#     execute_steps(shade_export_plan, df=shade_data)

#     # export non-shade data frame
#     non_shade_export_plan = cfg["exports"]["non_shade"]
#     execute_steps(non_shade_export_plan, df=non_shade_data)

def main_refactor():
    import pandas as pd
    from readers.xlReader import read_safely
    from pathlib import Path
    dir = Path(r"C:\Users\eddiec11us\Documents\tests\October 2024")
    frames: list[pd.DataFrame] = read_safely(src=dir, stack=True)
    stacked = pd.concat(frames)
    

if __name__ == "__main__":
    raise SystemExit(main_refactor())


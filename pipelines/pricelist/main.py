
from dotenv import load_dotenv
import pandas as pd

from config.paths import PRICE_LIST_YAML, CONFIG_DOT_ENV
from file_reader.dir_to_df import dir_to_df
from plan_executor.executor import DataPlanExecutor
from plan_executor.yaml_reader import import_data_plan

load_dotenv(dotenv_path=CONFIG_DOT_ENV)

def main():

    """
    read YAML
    execute YAML
    All actions should be in YAML
    
    """

    all_prices_cfg = {
        "directory": r"",
        "recursive": False,
        "suffixes": [".csv"],
        "add_source": False
        }

    # capture all data frames [expected: CSV] and concat
    all_prices: pd.DataFrame = dir_to_df(all_prices_cfg)

    # filter frames into shade and non-shade
    shade_data_plan: dict = import_data_plan(SHADE_YAML, plan_key="data_plan")
    price_list_plan: dict = 
    shade_data = DataPlanExecutor(all_prices, data_plan=shade_data_plan).processed_data

    print(shade_data.head())
    print(f"\n{shade_data.info()}")

if __name__ == "__main__":
    raise SystemExit(main())

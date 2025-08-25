# standard library imports

# Third party imports
import pandas as pd

# Internal Application Imports
from config.paths import PRICE_LIST_YAML
from utils.yaml_loader import load_yaml # also loads dotenv secrets
from plan_executor.executor import execute_steps

def main():

    """
    read YAML
    execute YAML
    """
    # load entire configuration for process
    cfg = load_yaml(PRICE_LIST_YAML)
    
    # import data
    data_load_cfg = cfg["load"]
    df: pd.DataFrame = execute_steps(data_load_cfg)
    
    # manipulate shade data frame

    # manipulate non-shade data frame

    # export shade data frame

    # export non-shade data frame

if __name__ == "__main__":
    raise SystemExit(main())


# standard library imports
import logging
from pathlib import Path

# Third party imports
import pandas as pd
from dotenv import load_dotenv

# Internal Application Imports
from config.paths import ALL_SALES_ENV, ALL_SALES_YAML
from plan_executor.executor import execute_steps
from utils.logging_config import setup_logging
from utils.yaml_loader import load_yaml

setup_logging(level=logging.DEBUG)
logger = logging.getLogger(__name__)
load_dotenv(dotenv_path=Path(ALL_SALES_ENV))

def main():
    """Extract all sales from network files and load into duck db"""
    cfg = load_yaml(ALL_SALES_YAML)

    # load all sales into duck db
    load_plan = cfg["load"]
    execute_steps(load_plan)

if __name__ == "__main__":
    raise SystemExit(main())

# python -m pipelines.all_sales.main
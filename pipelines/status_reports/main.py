"""Primary runner for status report pipeline"""
from os import getenv
from pathlib import Path
from dotenv import load_dotenv

from config.internal_paths import STATUS_REPORTS_CFG, STATUS_REPORTS_ENV
from pipelines.status_reports.sales_refresh import refresh_data
from utils.yaml_loader import load_yaml

def main():

    load_dotenv(STATUS_REPORTS_ENV)

    cfg = load_yaml(STATUS_REPORTS_CFG)

    refresh_data(
        data_cfg=cfg["data"], 
        database=cfg["paths"]["database"]
    )

if __name__ == "__main__":
    main()


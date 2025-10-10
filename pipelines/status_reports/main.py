"""Primary runner for status report pipeline"""
from os import getenv
from pathlib import Path
from dotenv import load_dotenv

from config.internal_paths import STATUS_REPORTS_CFG, STATUS_REPORTS_ENV
from pipelines.status_reports.sales_refresh import refresh_data
from utils.yaml_loader import load_yaml
from pipelines.status_reports.data_map import get_data_map
from pipelines.status_reports.xlwriter import generate_reports

import duckdb

REPORT_TIMEFRAME = "September 2025"

def main():

    load_dotenv(STATUS_REPORTS_ENV)

    cfg = load_yaml(STATUS_REPORTS_CFG)

    with duckdb.connect(cfg["paths"]["database"]) as conn:
        
        refresh_data(data_cfg=cfg["data"], conn=conn)
        
        report_maps = get_data_map(
            conn=conn, 
            report_cfg=cfg["report_map"],
            timeframe=REPORT_TIMEFRAME
        )

    generate_reports(
        report_maps=report_maps,
        templates=cfg["paths"]["templates"],
        out_dir=Path(cfg["paths"]["out_dir"]),
    )

if __name__ == "__main__":
    main()
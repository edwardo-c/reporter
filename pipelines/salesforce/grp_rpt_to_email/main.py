"""
emails count from salesforce report
expected to have user_email in the grouping
"""

from data_toolkit.salesforce.client import SFClient
from utils.yaml_loader import load_yaml
from dotenv import load_dotenv

from pipelines.paths.cfg_paths import SALESFORCE_GRP_RPT_TO_EMAIL_CFGS
from config.paths import SF_GRP_EMAILS_ENV

from data_toolkit.salesforce.reports_tabular.column_map import ColumnMap
from data_toolkit.salesforce.reducers.grouped_to_agg import single_grp_to_agg

"""file name of the config to use for the pipeline"""
CFG_FILE_NAME = "overdue_opps.yaml"


def main():

    load_dotenv(SF_GRP_EMAILS_ENV)

    cfg = load_yaml(SALESFORCE_GRP_RPT_TO_EMAIL_CFGS / CFG_FILE_NAME)

    # always exclude details to ensure factMap contains only aggregates
    payload = (
        SFClient(**cfg["credentials"])
            .get_report(
                report_id=cfg["report"]["id"],
                include_details=False
            )
        )

    column_map = ColumnMap(payload)

    if len(column_map.grp_keys_to_idx) > 1:
        raise NotImplementedError(
            f"Nested groupings detected in salesforce report. "
            "This pipeline currently supports single grouped reports only"
        )
    
    # guard rail against unexpected group key
    try:
        grp_key = cfg["report"]["grp_key"]
        grp_idx = column_map._get_grp_index_by_key(grp_key)
    except KeyError:
        raise KeyError(
            f"Unexpected group key! Expected: '{grp_key}', "
            f"got {list(column_map.grp_keys_to_idx.keys())[0]}. "
            f"config may be incorrect or "
            f"grouped columns in report are not as expected"
        )
    
    # guard rail against unexpected aggregate key
    try:
        agg_key = cfg["report"]["agg_key"]
        agg_idx = column_map._get_agg_index_by_key(agg_key)
    except KeyError:
        raise KeyError(
            f"Unexpected aggregate key! Expected: '{agg_key}', "
            f"got {list(column_map.agg_keys_to_idx.keys())[0]}. "
            f"config may be incorrect or "
            f"aggregate columns in report are not as expected"
        )
    
    
    email_to_row_count: dict = single_grp_to_agg(payload)

    breakpoint()

if __name__ == "__main__":
    main()
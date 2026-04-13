
from dotenv import load_dotenv

from config.paths import SF_GRP_EMAILS_ENV
from data_toolkit.clients._outlook.outlook_sender import BaseEmail
from data_toolkit.clients._outlook.outlook_sender import send_emails
from data_toolkit.salesforce.client import SFClient
from data_toolkit.salesforce.reducers.grouped_to_agg import single_grp_to_agg
from data_toolkit.salesforce.reports_tabular.column_map import ColumnMap
from pipelines.salesforce.grp_rpt_to_email.email_bodies.registry import get_email_func
from pipelines.paths.cfg_paths import SALESFORCE_GRP_RPT_TO_EMAIL_CFGS
from utils.yaml_loader import load_yaml


"""file name of the config to use for the pipeline"""
CFG_FILE_NAME = "overdue_opps.yaml"

PROD = False

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
        grp_idx = column_map._get_grp_index_by_key("OWNER_EMAIL")
    except KeyError:
        raise KeyError(
            f"Unexpected group key! Expected: 'OWNER_EMAIL', "
            f"got {list(column_map.grp_keys_to_idx.keys())[0]}. "
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

    emails_to_send: list[BaseEmail] = []

    body_func = get_email_func(cfg["email"]["body_func_key"])

    for email_addr, agg_val in email_to_row_count.items():
        e = BaseEmail(
            recipients=email_addr,
            subject=cfg["email"]["subject"],
            body=body_func(agg_val),
        )
        emails_to_send.append(e)

    sent_count = send_emails(emails_to_send, prod=PROD)

if __name__ == "__main__":
    main()
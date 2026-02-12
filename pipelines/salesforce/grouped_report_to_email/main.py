"""
emails count from salesforce report
expected to have user_email in the grouping
"""

from data_toolkit.salesforce.client import SFClient
from utils.yaml_loader import load_yaml
from dotenv import load_dotenv

from pipelines.paths.cfg_paths import SALESFORCE_GRP_RPT_TO_EMAIL_CFGS
from config.paths import SF_GRP_EMAILS_ENV

"""file name of the config to use for the pipeline"""
CFG_FILE_NAME = "overdue_opps.yaml"


def main():

    load_dotenv(SF_GRP_EMAILS_ENV)

    cfg = load_yaml(SALESFORCE_GRP_RPT_TO_EMAIL_CFGS / CFG_FILE_NAME)

    payload = SFClient(**cfg["credentials"]).get_report(**cfg["report"])

    breakpoint()

if __name__ == "__main__":
    main()
from pathlib import Path

PROJECT_ROOT = Path(__file__).parents[2]

SALESFORCE_GRP_RPT_TO_EMAIL_CFGS = (
    PROJECT_ROOT / 
    "pipelines"  / 
    "salesforce" / 
    "grp_rpt_to_email" / 
    "cfgs"
)
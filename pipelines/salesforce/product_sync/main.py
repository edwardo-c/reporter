"""scaffolding for product sync procedure from Acumatica to Salesforce"""

from utils.acumatica_odata import get_acumatica_table
from utils.salesforce import get_salesforce_table
from utils.yaml_loader import load_yaml
from dotenv import load_dotenv
from config.paths import SALESFORCE_PRODUCT_SYNC_CFG, SALESFORCE_PRODUCT_SYNC_ENV

def new_item_map(record: dict) -> dict:
    """aranges an acumatica record to new salesforce record"""
    breakpoint()


def main():
    
    load_dotenv(SALESFORCE_PRODUCT_SYNC_ENV)
    cfg = load_yaml(SALESFORCE_PRODUCT_SYNC_CFG)

    # truth table
    acumatica_cfg = cfg["acumatica"]
    acumatica_df = get_acumatica_table(
        url=acumatica_cfg["secrets"]["url"], 
        username=acumatica_cfg["secrets"]["username"],
        password=acumatica_cfg["secrets"]["password"], 
        params=acumatica_cfg["params"])

    # get salesforce data
    salesforce_cfg = cfg["salesforce"]
    salesforce_df = get_salesforce_table(
        username=salesforce_cfg["secrets"]["username"], 
        password=salesforce_cfg["secrets"]["password"], 
        security_token=salesforce_cfg["secrets"]["security_token"], 
        soql_query=salesforce_cfg["soql_query"])

    breakpoint()

    

    # identify missing parts

    # 

    ...

if __name__ == '__main__':
    main()


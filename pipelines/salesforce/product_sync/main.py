"""scaffolding for product sync procedure from Acumatica to Salesforce"""

from utils.acumatica_odata import get_acumatica_table
from utils.salesforce import get_salesforce_table
from utils.yaml_loader import load_yaml
from dotenv import load_dotenv
from config.paths import SALESFORCE_PRODUCT_SYNC_CFG, SALESFORCE_PRODUCT_SYNC_ENV
from pipelines.salesforce.product_sync.arrange import upload_new_parts
from simple_salesforce import Salesforce


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

    salesforce_cfg = cfg["salesforce"]
    sf = Salesforce(
        username=salesforce_cfg["secrets"]["username"],
        password=salesforce_cfg["secrets"]["password"],
        security_token=salesforce_cfg["secrets"]["security_token"])

    # get salesforce data
    salesforce_df = get_salesforce_table(sf=sf,
        soql_query=salesforce_cfg["soql_query"])

    upload_new_parts(
        sf=sf,
        acumatica_df=acumatica_df, 
        salesforce_df=salesforce_df,
        id_map=cfg["id_map"]
        )

if __name__ == '__main__':
    main()


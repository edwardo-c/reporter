"""static values"""
from data_toolkit.readers.sources import SFQuery, OData

ACCOUNT_PRICE_LIST_SOQL = """
SELECT 
  Id,
  Account__r.ACU_CUSTOMER_ID__c,
  Price_List__r.Customer_Price_Class__c,
  Price_List__r.Sales_Price_Group__r.Name,
  Price_List__r.ExternalID__c
FROM Account_Price_Lists__c
  WHERE Account__r.ACU_CUSTOMER_ID__c != NULL
  AND Price_List__r.ExternalID__c != NULL
"""

SOURCES = [
    OData(
        params={"$select": "CustID,PriceGroup,CustomerPriceClass", "$format":"json"},
        url="https://peerless-av.acumatica.com/OData/Peerless-AV/CustomerPriceGroupFeed",
        df_id="acu_cpg" # acumatica customer price groups
    ),
    SFQuery(
        soql=ACCOUNT_PRICE_LIST_SOQL,
        df_id="sf_cpg" # salesforce customer price groups
    ),
]

ENV_VAR_PATH=r"C:\Users\eddiec11us\dev_apps\reporter\config\secrets\sf_audit.env"
SQL_PATH = r"C:\Users\eddiec11us\dev_apps\reporter\scripts\salesforce_audit\customer_price_groups\compare_cust_price_class.sql"

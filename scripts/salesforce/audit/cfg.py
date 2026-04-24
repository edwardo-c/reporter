from data_toolkit.readers.sources import SFQuery, OData
from scripts.salesforce.audit.audit_obj import AuditObj

ENV_VAR_PATH=r"C:\Users\eddiec11us\dev_apps\reporter\config\secrets\sf_audit.env"
YAML_SETTINGS_PATH=r"C:\Users\eddiec11us\dev_apps\reporter\scripts\salesforce\audit\audit_settings.yaml"

# ===================================================
_PRODUCTS_SOQL = """
SELECT 
  Id,
  Name,
  Auth_Required__c,
  ACU_Item_Status__c, 
  ACU_PMPLCM__c,
  Category__c,
  Price_Group__r.Name,
  SF_IsActive__c
FROM Product2
"""

_PRICING_SOQL = """
SELECT  
  Product__r.Name,
  Price_List__r.Price_Group_Name__c,
  Price_List__r.Customer_Price_Class__c,
  Price_List_Price__c
FROM Price_List_Entry__c
WHERE 
  Active__c = TRUE 
  AND Price_List__r.Country_Office__c = 'US'
"""

_MSRP_SOQL = """
SELECT  
  Product2.Name,
  UnitPrice
FROM PricebookEntry
WHERE Pricebook2.Id = '01s6A000001t7RtQAI' 
  AND CurrencyIsoCode = 'USD'
  AND UnitPrice < 999999999
"""

PRODUCT_AUDIT_OBJ = AuditObj(
    sources=[
        SFQuery(soql=_PRODUCTS_SOQL, df_id="sf_products"),
        OData(
            params={}, 
            url=r"https://peerless-av.acumatica.com/OData/Peerless-AV/SOProductAudit", 
            df_id="acu_products"
        ),
        SFQuery(soql=_PRICING_SOQL, df_id="sf_price_list_entries"),
        SFQuery(soql=_MSRP_SOQL, df_id="sf_msrp")
    ],
    
    sql=r"C:\Users\eddiec11us\dev_apps\reporter\scripts\salesforce\audit\SQL\compare_products.sql",
    
    artifacts={
        "audited_products": r"C:\Users\eddiec11us\Desktop\SF_Audit_Files\product_fields.csv"
        ,
    }
)

# ================================================

_ACCOUNT_PRICE_LIST_SOQL = """
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

CPG_AUDIT_OBJ = AuditObj(
    sources=[
    OData(
        params={"$select": "CustID,PriceGroup,CustomerPriceClass", "$format":"json"},
        url="https://peerless-av.acumatica.com/OData/Peerless-AV/CustomerPriceGroupFeed",
        df_id="acu_cpg" # acumatica customer price groups
    ),
    SFQuery(
        soql=_ACCOUNT_PRICE_LIST_SOQL,
        df_id="sf_cpg" # salesforce customer price groups
    ),
],
    sql=r"C:\Users\eddiec11us\dev_apps\reporter\scripts\salesforce\audit\SQL\compare_cust_price_groups.sql",
    artifacts={"audited_cpg": r"C:\Users\eddiec11us\Desktop\SF_Audit_Files\customer_price_groups.csv",}
)

# =======================================================
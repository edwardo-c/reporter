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
  Price_Group__r.Name
FROM Product2
"""

_PRODUCTS_SOURCES = [
    SFQuery(soql=_PRODUCTS_SOQL, df_id="sf_products"),
    OData(
        params={
            "$format": "json", 
            "$select": "CleanedPartNumber,ItemStatus,PriceGroup,Category,ProductLifeCycleManagement,CleanedAuthRequired"}, 
        url=r"https://peerless-av.acumatica.com/OData/Peerless-AV/SOProductAudit", 
        df_id="acu_products")
]
_PRODUCTS_SQL = r"C:\Users\eddiec11us\dev_apps\reporter\scripts\salesforce\audit\SQL\compare_products.sql"
_PRODUCTS_OUT = r"C:\Users\eddiec11us\Desktop\SF_Audit_Files\products.csv"

PRODUCT_AUDIT_OBJ = AuditObj(
    sources=_PRODUCTS_SOURCES,
    sql=_PRODUCTS_SQL,
    final_name="audited_products",
    out_path=_PRODUCTS_OUT
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

_CPG_SOURCES = [
    OData(
        params={"$select": "CustID,PriceGroup,CustomerPriceClass", "$format":"json"},
        url="https://peerless-av.acumatica.com/OData/Peerless-AV/CustomerPriceGroupFeed",
        df_id="acu_cpg" # acumatica customer price groups
    ),
    SFQuery(
        soql=_ACCOUNT_PRICE_LIST_SOQL,
        df_id="sf_cpg" # salesforce customer price groups
    ),
]

_CPG_SQL = r"C:\Users\eddiec11us\dev_apps\reporter\scripts\salesforce\audit\SQL\compare_cust_price_class.sql"
_CPG_OUT = r"C:\Users\eddiec11us\Desktop\SF_Audit_Files\customer_price_groups.csv"

CPG_AUDIT_OBJ = AuditObj(
    sources=_CPG_SOURCES,
    sql=_CPG_SQL,
    final_name="audited_cpg",
    out_path=_CPG_OUT
)

# =======================================================
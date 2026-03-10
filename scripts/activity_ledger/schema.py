from data_toolkit.duckdb.union_all.contract_projection import Col

# contract enforced schema for imported data - required columns to build union all
# these are part of the data compilation step
INPUT_SCHEMA = [
    Col("SalesRepID18",   "VARCHAR", "NULL"),
    Col("ActivityCode",   "VARCHAR", "NULL"),
    Col('ActivityDate',   "DATE",    "NULL")
]

# Activity Ledger Output Schema
# used to normalize column dtypes, raises on missing columns
from data_toolkit.cleaners.df_dtypes.dtype import StrCol, IntCol, DateCol, ColError, DateFmt

OUTPUT_SCHEMA = [
    StrCol('Sales_Rep__c'),
    DateCol('Period_Start__c',  format = DateFmt.YYYY_MM_DD),
    StrCol('Period_Type__c'),
    IntCol('Total_Score__c', errors=ColError.RAISE),
    IntCol('Calls_Count__c', errors=ColError.RAISE),
    IntCol('Calls_Score__c', errors=ColError.RAISE),
    IntCol('Contacts_Count__c', errors=ColError.RAISE),
    IntCol('Contacts_Score__c', errors=ColError.RAISE),
    IntCol('Converted_Leads_Count__c', errors=ColError.RAISE),
    IntCol('Converted_Leads_Score__c', errors=ColError.RAISE),
    IntCol('Accounts_Count__c', errors=ColError.RAISE),
    IntCol('Accounts_Score__c', errors=ColError.RAISE),
    IntCol('Opportunities_Count__c', errors=ColError.RAISE),
    IntCol('Opportunities_Score__c', errors=ColError.RAISE),
    IntCol('In_Person_Events_Count__c', errors=ColError.RAISE),
    IntCol('In_Person_Events_Score__c', errors=ColError.RAISE),
    IntCol('Quotes_Count__c', errors=ColError.RAISE),
    IntCol('Quotes_Score__c', errors=ColError.RAISE),
    IntCol('Virtual_Events_Count__c', errors=ColError.RAISE),
    IntCol('Virtual_Events_Score__c', errors=ColError.RAISE),
]


from data_toolkit.salesforce.payload import ExternalID

EXTERNAL_ID = ExternalID(
    name="External_ID__c",
    id_parts=[
        'Sales_Rep__c',
        'Period_Start__c',
        'Period_Type__c'
        ]
    )
from data_toolkit.duckdb.union_all.contract_projection import Col

# contract enforced schema for imported data via SOQL
# required columns to build Activity Ledger Long Data
INPUT_SCHEMA = [
    Col("SalesRepID18",   "VARCHAR", "NULL"),
    Col("ActivityCode",   "VARCHAR", "NULL"),
    Col('ActivityDate',   "DATE",    "NULL")
]

# Activity Ledger Output Schema, columns required in Payload
# used to normalize column dtypes, raises on missing columns
from data_toolkit.cleaners.df_dtypes.dtype import StrCol, IntCol, DateCol, ColError, DateFmt

OUTPUT_SCHEMA = [
    StrCol('Sales_Rep__c'),
    DateCol('Period_Start__c',  format = DateFmt.YYYY_MM_DD),
    StrCol('Period_Type__c'),
    StrCol('Type__c'),
    StrCol('SubType__c'),
    StrCol('Activity__c'),
    IntCol('Activity_Count__c', errors=ColError.RAISE),
    IntCol('Activity_Score__c', errors=ColError.RAISE),
]

from data_toolkit.salesforce.payload import BulkObj

# Salesforce bulk object for upsert and concatenated External id key
BULK_OBJ = BulkObj(
    name="Activity_Ledger__c",
    external_id_name="External_ID__c",
    external_id_parts=tuple([
        'Sales_Rep__c',
        'Period_Start__c',
        'Period_Type__c',
        'Type__c',
        'SubType__c',
        'Activity__c'
    ])
)
  
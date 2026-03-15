
from dotenv import load_dotenv
from os import getenv
from config.paths import SF_ACTIVITIES_ENV

from data_toolkit.duckdb.sql_dir import SqlDir
from data_toolkit.duckdb.union_all_cfg import UnionAllCfg
from data_toolkit.duckdb.client import SQLCol
from data_toolkit.readers.context import ReaderContext
from simple_salesforce import Salesforce
from data_toolkit.readers.sources import SFQuery

load_dotenv(SF_ACTIVITIES_ENV)

CTX = ReaderContext(
    sf=Salesforce(
        username=getenv("SF_USERNAME"), 
        password=getenv("SF_PASSWORD"), 
        security_token=getenv("SF_TOKEN")
    )
)

from scripts.activity_ledger.SOQL.registry import get_query, load_queries

load_queries()

SOURCES = [
    SFQuery(soql=get_query("events"), df_id="raw_meeting_events"),
    SFQuery(soql=get_query("contacts"), df_id="raw_new_contacts"),
    SFQuery(soql=get_query("opportunities"), df_id="raw_new_opps"),
    SFQuery(soql=get_query("accounts"), df_id="raw_new_accts"),
    SFQuery(soql=get_query("quotes"), df_id="raw_new_quotes"),
    SFQuery(soql=get_query("leads"), df_id="raw_converted_leads"),
    SFQuery(soql=get_query("calls"), df_id="raw_calls")
]

SQL_DIR = SqlDir(getenv("SQL_BASE_DIR"))

ORDERED_SQL = SQL_DIR.paths_list(
    [
        "scoring", 
        "events", 
        "contacts", 
        "opps", 
        "accts", 
        "quotes", 
        "leads", 
        "calls"
    ]
)

UNION_ALL_CFG = UnionAllCfg(
    name="ActivityLedger",

    schema=[
        SQLCol("SalesRepID18",   "VARCHAR", "NULL"),
        SQLCol("ActivityCode",   "VARCHAR", "NULL"),
        SQLCol('ActivityDate',   "DATE",    "NULL")
    ],
    branches=[
        "new_contacts", 
        "new_opps", 
        "new_accts", 
        "new_quotes", 
        "new_leads", 
        "new_calls", 
        "new_events",
    ]
)


# ============ not yet ready to refactor this part ====================

from data_toolkit.cleaners.df_dtypes.dtype import StrCol, IntCol, DateCol, ColError, DateFmt

OUTPUT_SCHEMA = [
    StrCol('Sales_Rep__c'),
    DateCol('Period_Start__c',  format = DateFmt.YYYY_MM_DD),
    StrCol('Period_Type__c'),
    StrCol('Type__c'),
    StrCol('Sub_Type__c'),
    StrCol('Activity__c'),
    IntCol('Activity_Count__c', errors=ColError.RAISE),
    IntCol('Activity_Score__c', errors=ColError.RAISE),
]

from data_toolkit.salesforce.payload.payload import BulkObj

# Salesforce bulk object for upsert and concatenated External id key
BULK_OBJ = BulkObj(
    name="Activity_Ledger__c",
    external_id_name="External_ID__c",
    external_id_parts=tuple([
        'Sales_Rep__c',
        'Period_Start__c',
        'Period_Type__c',
        'Type__c',
        'Sub_Type__c',
        'Activity__c'
    ])
)
  
from os import getenv
from dotenv import load_dotenv
from config.paths import SF_OVERDUE_OPPS_ENV

from simple_salesforce import Salesforce

from data_toolkit.readers.context import ReaderContext

load_dotenv(SF_OVERDUE_OPPS_ENV)

CTX = ReaderContext(
    sf=Salesforce(
        username=getenv("SF_USERNAME"), 
        password=getenv("SF_PASSWORD"), 
        security_token=getenv("SF_TOKEN")
    )
)
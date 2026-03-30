from scripts.pricelist_emailer import config
from data_toolkit.readers.context import ReaderContext
from simple_salesforce import Salesforce
from os import getenv

READER_CTX = ReaderContext(
        sf=Salesforce(
            username=getenv(config.SF_CRED.username), 
            password=getenv(config.SF_CRED.password),
            security_token=getenv(config.SF_CRED.token)
        )
    )



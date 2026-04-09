from scripts.pricelist.emailer import config
from scripts.pricelist.PathBuilder.path_builder import PriceListPathBuilder
from data_toolkit.readers.context import ReaderContext
from simple_salesforce import Salesforce
from os import getenv
from data_toolkit.clients.acumatica import autheticated_session

READER_CTX = ReaderContext(
    sf=Salesforce(
        username=getenv(config.SF_CRED.username), 
        password=getenv(config.SF_CRED.password),
        security_token=getenv(config.SF_CRED.token)
    ),
    acu=autheticated_session(
        getenv(config.ACU_CRED.username), 
        getenv(config.ACU_CRED.password)
    )
)

APP_DIR_PATH_BUILDER = PriceListPathBuilder(root=getenv("APP_FOLDER_ROOT_DIR"))
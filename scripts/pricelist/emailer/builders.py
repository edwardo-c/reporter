# External connections to outside apps

from os import getenv

from simple_salesforce import Salesforce

from data_toolkit.clients.acumatica import autheticated_session
from data_toolkit.clients import outlook
from data_toolkit.readers.context import ReaderContext
from scripts.pricelist.emailer.secrets import PriceListEnvVars

OUTLOOK = outlook.get_outlook()

def get_reader_ctx(env_vars: PriceListEnvVars) -> ReaderContext:
    return ReaderContext(
        sf=Salesforce(
            username=env_vars.sf_user, 
            password=env_vars.sf_pw,
            security_token=env_vars.sf_token
        ),
        acu=autheticated_session(
            env_vars.acu_user, 
            env_vars.acu_pw
        )
    )
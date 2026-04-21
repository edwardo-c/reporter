"""third party connections"""
from data_toolkit.readers.context import ReaderContext
from simple_salesforce import Salesforce
from data_toolkit.clients.acumatica import autheticated_session
from scripts.salesforce.audit.secrets import SyncCredentials

def get_reader_ctx(env_vars: SyncCredentials) -> ReaderContext:
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
from dataclasses import dataclass
from dotenv import load_dotenv
from os import getenv

from utils.validators import normalize_path

@dataclass
class SyncCredentials:
    sf_user: str
    sf_pw: str
    sf_token: str
    acu_user: str
    acu_pw: str

def load_env_vars(env_var_path: str) -> SyncCredentials:
    
    load_dotenv(normalize_path(env_var_path))

    return SyncCredentials(
        sf_user=getenv("SF_USER"),
        sf_pw=getenv("SF_PW"),
        sf_token=getenv("SF_TOKEN"),
        acu_user=getenv("ACU_USER"),
        acu_pw=getenv("ACU_PW")
    )
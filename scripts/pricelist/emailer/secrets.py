from dataclasses import dataclass
from dotenv import load_dotenv
from enum import Enum
from os import getenv

from utils.validators import normalize_path

class EnvVarStr(Enum):
    APP_ROOT = "APP_FOLDER_ROOT_DIR"
    SF_USER = "SF_USER"
    SF_PW = "SF_PW"
    SF_TOKEN = "SF_TOKEN"
    ACU_USER = "ACU_USERNAME"
    ACU_PW = "ACU_PW" 
    YAML_INPUT = "USER_INPUT_YAML_PATH"

@dataclass
class PriceListEnvVars:
    root: str
    sf_user: str
    sf_pw: str
    sf_token: str
    acu_user: str
    acu_pw: str
    yaml: str

def load_env_vars(
        env_var_path: str
) -> PriceListEnvVars:
    
    load_dotenv(normalize_path(env_var_path))

    return PriceListEnvVars(
        root=getenv(EnvVarStr.APP_ROOT.value),
        sf_user=getenv(EnvVarStr.SF_USER.value),
        sf_pw=getenv(EnvVarStr.SF_PW.value),
        sf_token=getenv(EnvVarStr.SF_TOKEN.value),
        acu_user=getenv(EnvVarStr.ACU_USER.value),
        acu_pw=getenv(EnvVarStr.ACU_PW.value),
        yaml=getenv(EnvVarStr.YAML_INPUT.value)
    )
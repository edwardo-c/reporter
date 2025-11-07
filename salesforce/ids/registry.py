from utils.yaml_loader import load_yaml
from config.paths import PRICE_GROUP_ID_PATH


PRICE_GROUP_IDS: dict = load_yaml(PRICE_GROUP_ID_PATH)["price_grp"]

def price_grp_id(grp: str) -> str:
    return PRICE_GROUP_IDS.get(grp, None) 

    
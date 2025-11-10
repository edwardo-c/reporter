from utils.yaml_loader import load_yaml
from config.paths import PRICE_GROUP_ID_PATH, PRICE_LVL_PATH

price_lvl_cfg = load_yaml(PRICE_LVL_PATH)

PRICE_GROUP_IDS: dict = load_yaml(PRICE_GROUP_ID_PATH)["price_grp"]

MSRP_ID = price_lvl_cfg["standard_price_book"]

def price_grp_id(grp: str) -> str:
    return PRICE_GROUP_IDS.get(grp, None) 

    
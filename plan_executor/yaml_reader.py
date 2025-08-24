from pathlib import Path
import yaml

def import_data_plan(path: str | Path, plan_key: str = "data_plan"):
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg.get(plan_key, [])
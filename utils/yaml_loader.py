import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path("config.config.env"))

def load_yaml(path):
    raw = Path(path).read_text(encoding="utf-8")
    # expand ${VAR} and defaults ${VAR:default}
    def sub(match):
        key, _, default = match.group(1).partition(":")
        return os.getenv(key, default)
    
    import re
    raw = re.sub(r"\$\{([^}]+)\}", sub, raw)
    return yaml.safe_load(raw)

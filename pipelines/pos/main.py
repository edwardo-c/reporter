from readers.xlReader import read_safely
from utils.yaml_loader import load_yaml
from dotenv import load_dotenv
from config.paths import POS_DOT_ENV, POS_YAML

from pathlib import Path

load_dotenv(dotenv_path=Path(POS_DOT_ENV))


def main():
    # load yaml
    cfg = load_yaml(POS_YAML)
    files_cfg = cfg["files"]

    # TODO: load data frame using cfg

    for file_meta in files_cfg:
        print(file_meta)

if __name__ == "__main__":
    main()
# standard library imports
from dotenv import load_dotenv
import os
from pathlib import Path

# Third party imports
import pandas as pd

# Internal Imports
from readers.xlReader import read_safely
from pipelines.pricelist.split_into_csvs.csv_partitioner import run
from config.paths import PRICE_LIST_ENV

def main():

    print(f"Splitting CSVs")

    load_dotenv(PRICE_LIST_ENV)

    out_map = {
        "Neptune": os.getenv("NEP_OUT"), 
        "Peerless-AV": os.getenv("PAV_OUT")}

    frames = read_safely(os.getenv("SRC"), stack=True)
    
    run(frames, out_map=out_map)

    print(f"Process Complete")

if __name__ == "__main__":
    raise SystemExit(main())


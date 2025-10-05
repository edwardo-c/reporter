import pytest
from pathlib import Path
import os

import pandas as pd

from pipelines.pricelist.split_into_csvs import csv_partitioner as ep

def test_brand_col():
    
    df = pd.DataFrame(
            {'part':['nep', 'pav'], 
             'Price Group': ['NEPTUNE', 'NOT NEPTUNE']})
    expected = pd.DataFrame(
            {'part':['nep', 'pav'], 
             'Price Group': ['NEPTUNE', 'NOT NEPTUNE'],
             'brand': ['Neptune', 'Peerless-AV']})
    
    result = ep.add_brand_column(df=df)
    
    pd.testing.assert_frame_equal(result, expected)

def test_partition(tmp_path):
    
    # Arrange
    df = pd.DataFrame(
            {'Customer':['A', 'A', 'B'], 
             'Price Group': ['NEPTUNE', 'NOT NEPTUNE', 'NOT NEPTUNE']})
    
    branded = ep.add_brand_column(df=df)
    
    # temporary landing directories
    sub_pav = tmp_path / 'pav'
    sub_nep = tmp_path / "nep"

    os.mkdir(str(sub_pav))
    os.mkdir(str(sub_nep))

    # Act
    ep.export_partitioned_csv(branded, {"Peerless-AV": sub_pav, "Neptune": sub_nep})

    # assert
    def file_count(dir: str) -> int:
        return len([
            f
            for f in os.listdir(dir)
            if (Path(dir) / f).is_file()
        ])

    # file count in each
    assert file_count(sub_nep) == 1
    assert file_count(sub_pav) == 2

    pav_df_A = pd.read_csv(sub_pav / "A.csv")
    pav_df_B = pd.read_csv(sub_pav / "B.csv")
    nep_df_A = pd.read_csv(sub_nep / "A.csv")

    assert len(pav_df_A) == 1
    assert len(pav_df_B) == 1
    assert len(nep_df_A) == 1



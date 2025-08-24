from pathlib import Path
import pytest
import os

import pandas as pd

from file_reader.dir_to_df import dir_to_df

# empty directory raises
def test_empty_dir(tmp_path: Path):
    with pytest.raises(ValueError):
        dir_to_df({'directory': tmp_path, 'suffixes': ['.csv']})

# path is not a directory
def test_not_a_dir(tmp_path):
    f = tmp_path / "t.csv"
    f.write_text("x\n1", encoding="utf-8")
    with pytest.raises(ValueError):
        dir_to_df({'directory': f})

# concat two csvs, non-recursive
def test_concat_csv_non_recursive(tmp_path: Path):
    (tmp_path / "a.csv").write_text("x,y\n1,10\n", encoding="utf-8")
    (tmp_path / "b.csv").write_text("x,y\n2,20\n", encoding="utf-8")
    df: pd.DataFrame = dir_to_df({
            "directory": tmp_path,
            "recursive": False,
            "suffixes": [".csv"],
            "add_source": True
    })
    assert len(df) == 2
    assert set(df.columns) == {"x", "y", "__source_file"}
    assert set(df["__source_file"].unique()) == {"a.csv", "b.csv"}

def test_non_recursive_ignores_subfolders(tmp_path: Path):
    (tmp_path / "a.csv").write_text("x\n1\n", encoding="utf-8")
    sub = tmp_path / "sub"; sub.mkdir()
    (sub / "sub.csv").write_text("x\n2\n", encoding="utf-8")
    df = dir_to_df({"directory": tmp_path, "recursive": False, "suffixes": ['.csv']})
    assert len(df) == 1

def test_recursive_accepts_subfolders(tmp_path: Path):
    (tmp_path / "a.csv").write_text("x\n1\n", encoding="utf-8")
    sub = tmp_path / "sub"; sub.mkdir()
    (sub / "sub.csv").write_text("x\n2\n", encoding="utf-8")
    df = dir_to_df({"directory": tmp_path, "recursive": True, "suffixes": ['.csv']})
    assert len(df) == 2

def test_mixed_columns_union(tmp_path: Path):
    (tmp_path / "a.csv").write_text("x,y\n1,10\n", encoding="utf-8")
    (tmp_path / "b.csv").write_text("x,z\n2,30\n", encoding="utf-8")

    df = dir_to_df({"directory": str(tmp_path), "suffixes": [".csv"]})
    # unioned columns, missing filled with NaN
    assert set(df.columns) == {"x", "y", "z", "__source_file"}
    assert df.isna().sum().loc[["y", "z"]].sum() >= 1
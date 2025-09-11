import pytest

import pandas as pd

from readers.safe_reader import read_safely
from readers.safe_reader import PathCFG

def test_missing_src_path(tmp_path):
    df = pd.DataFrame({"X": [1], "Y": [10]})
    out_path = tmp_path / "t.xlsx"
    df.to_excel(out_path, index=False)
    cfg: PathCFG = {'error': out_path}
    with pytest.raises(KeyError): 
        read_safely(cfg)

def test_use_cols(tmp_path):
    df = pd.DataFrame({"X": [1], "Y": [10], "Z": [20]})
    out_path = tmp_path / "t.xlsx"
    df.to_excel(out_path, index=False)
    cfg: PathCFG = {"src_path": out_path, "use_cols": ["X", "Z"]}
    df = read_safely(cfg=cfg)
    assert {"X", "Z"}.issubset(df.columns)

def test_missing_reader(tmp_path):
    df = pd.DataFrame({"X": [1], "Y": [10], "Z": [20]})
    out_path = tmp_path / "t.xlsm"
    df.to_excel(out_path, index=False)
    cfg: PathCFG = {"src_path": out_path}
    with pytest.raises(NameError):
        df = read_safely(cfg=cfg)
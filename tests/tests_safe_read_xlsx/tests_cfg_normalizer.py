import pytest
import logging

import pandas as pd

from plan_executor.operations.xlsx_reader import _config_normalizer, _column_rename, read_xlsx
from config.paths import TEST_XLSX

logging.basicConfig(level=logging.INFO)

def test_invalid_arg():
    
    # invalid data type
    with pytest.raises(TypeError):
        my_int = 1
        _config_normalizer(my_int)

    # invalid key name
    with pytest.raises(ValueError):
        invalid_cfg = {"foo": "bar"}
        _config_normalizer(invalid_cfg)
    
    # invalid path
    with pytest.raises(FileNotFoundError):
        invalid_cfg = {"path": "foo.bar.xlsx"}
        _config_normalizer(invalid_cfg)

    # missing alias for multiple files
    with pytest.raises(ValueError):
        missing_als = [{"path": TEST_XLSX, "alias": "a1"},
                       {"path": TEST_XLSX}]
        _config_normalizer(missing_als)

def test_rename_map():
    data = pd.DataFrame({"spam": [1,2,3], "eggs": [10,20,30]})
    result = _column_rename(data, {"spam": "SPAM", "eggs":"EGGS"})
    assert ("SPAM", "EGGS") == tuple(result.columns)

def test_single_str(tmp_path):
    data = pd.DataFrame({"spam": [1,2,3], "eggs": [10,20,30]})
    p = tmp_path / "t.xlsx"
    data.to_excel(p, index=False)
    result: list = read_xlsx(p)
    result_data = result[0]["data"]
    assert isinstance(result_data, pd.DataFrame) # check if data is a dataframe
    pd.testing.assert_frame_equal(data, result_data)

def test_multiple_cfg(tmp_path):
    # create first workbook
    data_1 = pd.DataFrame({"spam": [1,2,3], "eggs": [10,20,30], "fizz": [40,50,60]})
    p_1 = tmp_path / "t_1.xlsx"
    data_1.to_excel(p_1, index=False)
    
    # create second workbook
    data_2 = pd.DataFrame({"mom": [9,8,7], "dad": [90,80,70], "sis": [60,50,40]})
    p_2 = tmp_path / "t_2.xlsx"
    data_2.to_excel(p_2, index=False)

    cfg = [
        {"path": p_1, "alias": "data_1", "usecols" : ["spam", "eggs"]}, # config 1
        {"path": p_2, "alias": "data_2"}, # config 2
    ] 

    data_1_expected = pd.DataFrame({"spam": [1,2,3], "eggs": [10,20,30]})

    results: dict = read_xlsx(cfg)

    r_data_1 = results[0]["data"]
    r_data_2 = results[1]["data"]

    pd.testing.assert_frame_equal(data_1_expected, r_data_1)
    pd.testing.assert_frame_equal(data_2, r_data_2)


    
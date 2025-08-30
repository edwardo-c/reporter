import pytest

import pandas as pd

from plan_executor.operations.xlsx_reader import _config_normalizer
from config.paths import TEST_XLSX

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

def test_reader():
    ...    

    
import pytest

import pandas as pd

from plan_executor.operations.xlsx_reader import _config_normalizer

# def test_cfg_normalizer(tmp_path):
#     df = pd.DataFrame(
#         {"col_a": [1, 2, 3],
#          "col_b": [4, 5, 6]
#         })
#     df.to_excel(tmp_path / "t.xlsx")

def test_invalid_arg():
    
    with pytest.raises(TypeError):
        my_int = 1
        _config_normalizer(my_int)

    # invalid_cfg = {"foo": "bar"}
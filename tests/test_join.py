import pandas as pd
import pytest

from plan_executor.operations.join import join

def test_invalid_right():
    with pytest.raises(TypeError):
        join(pd.DataFrame(), right='invalid', how='', on=[])
import logging
import pytest

import pandas as pd
import numpy as np

from plan_executor.operations.cond_drop import drop_null_dups

logging.basicConfig(level=logging.INFO)

def test_drop_null_dups_prefer_null():
    """drop row where condition = true"""
    # Arrange
    df = pd.DataFrame(
        {
            "cust": ["c01", "c01", "c02"],
            "part": ["p01", "p01", "p01"],
            "cls" : ["cs1", np.nan, "cs1"],
            "cost": [5, 1, 5],
        }
    )

    expected = pd.DataFrame(
        {
            "cust": ["c01", "c02"],
            "part": ["p01", "p01"],
            "cls" : [np.nan, "cs1"],
            "cost": [1, 5],
        }
    )

    cfg = {
        "null_col": "cls",
        "keep_null": True,
        "subset": ["cust", "part"]
    }

    # Act
    result = drop_null_dups(df, cfg)

    # Assert
    pd.testing.assert_frame_equal(result, expected)

def test_drop_null_dups_prefer_non_null():
    # Arrange
    df = pd.DataFrame(
        {
            "cust": ["c01", "c01", "c02"],
            "part": ["p01", "p01", "p01"],
            "cls" : ["cs1", np.nan, "cs1"],
            "cost": [5, 1, 5],
        }
    )

    expected = pd.DataFrame(
        {
            "cust": ["c01", "c02"],
            "part": ["p01", "p01"],
            "cls" : ["cs1", "cs1"],
            "cost": [5, 5],
        }
    )

    cfg = {
        "null_col": "cls",
        "keep_null": False,
        "subset": ["cust", "part"]
    }

    # Act
    result = drop_null_dups(df, cfg)

    # Assert
    pd.testing.assert_frame_equal(result, expected)

    # pytest .\tests\test_cond_drop.py --log-cli-level=INFO
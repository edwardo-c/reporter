import logging
import pytest

import pandas as pd
import numpy as np

from plan_executor.operations.stack_frames import (
    _missing_fields,
    stack_frames
)
from utils.logging_config import setup_logging

setup_logging(level=logging.WARNING)
logger = logging.getLogger(__name__)

def test_frame_stacking():
    """test frame stacking, raise errors for mismatch"""
    # Arrange
    data_1 = pd.DataFrame(
        {"col_a": ["a"], "col_b": ["b"]}
    )

    data_2 = pd.DataFrame(
        {"col_a": ["a"], "col_c": ["c"]}
    )
    
    frames = [
        {"alias": "data_1", "data": data_1},
        {"alias": "data_2", "data": data_2}
    ]

    schema = ["col_a", "col_b", "col_c"]

    result = stack_frames(frames, schema=schema, source=False)

    logging.debug(f"{result}")

    expected = pd.DataFrame({
        "col_a": ["a", "a"], 
        "col_b": ["b", np.nan], 
        "col_c": [np.nan, "c"]})

    pd.testing.assert_frame_equal(result, expected)

def test_missing_fields():
    """Pass missing fields, expecting raised value error"""
    # Arrange
    data_1 = pd.DataFrame(
        {"missing_a": [1, 2, 3], "missing_b": [4, 5, 6]}
    )

    data_2 = pd.DataFrame(
        {"col_a": [1, 2, 3], "missing_b": [4, 5, 6]}
    )
    
    schema = ["col_a", "col_b"]

    expected = [
        {"alias": "data_1", "missing": ["col_a", "col_b"]},
        {"alias": "data_2", "missing": ["col_b"]}
    ]

    frames = [
        {"alias": "data_1", "data": data_1},
        {"alias": "data_2", "data": data_2}
    ]

    # Act
    missing = _missing_fields(frames=frames, schema=schema)

    logger.debug("missing return value: %s", missing)    

    # Assert
    assert missing == expected

    

import logging
import pytest

import pandas as pd

from plan_executor.operations.stack_frames import (
    _missing_fields,
    stack_frames
)
from utils.logging_config import setup_logging

setup_logging(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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

def test_strict_mode():
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
    with pytest.raises(ValueError):
        stack_frames(frames=frames, schema=schema, strict=True)  
    

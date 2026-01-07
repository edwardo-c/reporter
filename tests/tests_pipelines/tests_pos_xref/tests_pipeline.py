import pytest

import pandas as pd

from pipelines.pos_xref.xref import PosXref

@pytest.fixture
def data_a():
    yield pd.DataFrame(
        [
            ('drop', '01111'),
            ('keep', '60502')
        ],
        columns=['cust', 'zip']
    )

@pytest.fixture
def data_b():
    yield pd.DataFrame(
        [
            ('keep', '60502')
        ],
        columns=['CUST', 'ZIP']
    )

def test_multiple_col_join(data_a, data_b):
    """
    Given provided columns, which rows exist in left that do not in right
    """
    
    join_columns = {'cust':'CUST', 'zip':'ZIP'}
    pos_xref = PosXref(data_a, data_b, join_columns)
    result = pos_xref._inner_join()

    expected = pd.DataFrame(
        [
            ('keep', '60502')
        ],
        columns=['cust', 'zip']
    )

    pd.testing.assert_frame_equal(result, expected)

def test_single_col_join(data_a, data_b):
    
    join_columns = {'cust':'CUST'}
    pos_xref = PosXref(data_a, data_b, join_columns)
    result = pos_xref._inner_join()

    expected = pd.DataFrame(
        [
            ('keep', '60502')
        ],
        columns=['cust', 'zip']
    )
    pd.testing.assert_frame_equal(result, expected)

def test_deduped_left(data_b):
    
    duped_df = pd.DataFrame(
        [
            ('dup', '01111'),
            ('dup', '01111'),
            ('not_dup', '60502')
        ],
        columns=['cust', 'zip']
    )

    join_columns = {'cust':'CUST', 'zip':'ZIP'}
    pos_xref = PosXref(duped_df, data_b, join_columns=join_columns)
    
    result = pos_xref.left_df

    expected = pd.DataFrame(
        [
            ('dup', '01111'),
            ('not_dup', '60502')
        ],
        columns=['cust', 'zip']
    )

    pd.testing.assert_frame_equal(result, expected)

    
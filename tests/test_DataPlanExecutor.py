# standard library imports
import logging
import pytest

# third party imports
import pandas as pd

# application imports
from plan_executor.executor import DataPlanExecutor
from plan_executor import registry

logging.basicConfig(level=logging.INFO)

def gen_test_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            'colA': ['A', 'A', 'C'],
            'colB': ['group1', 'group1', 'group2']
            }
        )


def test_groupby():
    test_data = gen_test_data()

    data_plan = [
        {
            "op": "groupby",
            "args": {
                "by":"colA"
            }
        },
    ]

    e = DataPlanExecutor(test_data, data_plan)
    e.run()
    
    grouped_data = e.processed_data

    
    for group, data in grouped_data:
        assert group == 'A' or group == 'C'
        if group == 'A':
            assert len(data) == 2
        if group == 'C':
            assert len(data) == 1

def test_filter_in():
    """test for 'filer' step of DataPlanExecutor class"""
    test_data = gen_test_data()
    
    data_plan = [
        {
            "op": "filter",
            "args": {
                "col":"colA",
                "val":"a",
                "case_insensative": True
            }
        },
    ]

    e = DataPlanExecutor(test_data, data_plan)
    e.run()

    result: pd.DataFrame = e.processed_data

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert all(col in result.columns for col in ['colA', 'colB'])
    assert (result['colA'] == 'A').all()

    # pytest .\tests\test_DataPlanExecutor.py

def test_filter_out():
    """test for 'filer' step of DataPlanExecutor class"""
    test_data = gen_test_data()
    
    data_plan = [
        {
            "op": "filter",
            "args": {
                "col":"colA",
                "val":"a",
                "case_insensative": True,
                "filter_in": False
            }
        },
    ]

    e = DataPlanExecutor(test_data, data_plan)
    e.run()

    result: pd.DataFrame = e.processed_data

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
    assert all(col in result.columns for col in ['colA', 'colB'])
    assert (result['colA'] != 'A').all()
# standard library imports
import logging
import pytest

# third party imports
import pandas as pd

# application imports
from plan_executor.executor import DataPlanExecutor
from plan_executor import transforms

logging.basicConfig(level=logging.INFO)

def test_groupby():
    test_data = pd.DataFrame(
        {
            'colA': ['A', 'A', 'C'],
            'colB': ['group1', 'group1', 'group2']
            }
        )

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
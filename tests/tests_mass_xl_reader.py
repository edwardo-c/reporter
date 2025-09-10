import pytest
import logging

import pandas as pd

from utils.logging_config import setup_logging

from plan_executor.operations.mass_xl_reader import MassXlReader

setup_logging(level=logging.WARNING)
logger = logging.getLogger(__name__)

def test_global_rename_map():
    data = pd.DataFrame({
          "CUST NAME": ['a', 'b', 'c'],
          "MFG PART" : ['z', 'y', 'x']
    }) 
    grm = {
        "CustomerName": ["CUST NAME", "customer name"],
        "PartNumber": ["MFG PART", "inventory id"] 
      }
      
    result = MassXlReader.rename_map_from_global(data, grm)
    assert result == {'CustomerName': 'CUST NAME', 'PartNumber': 'MFG PART'}
    
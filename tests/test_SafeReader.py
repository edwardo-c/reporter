"""Pytest for SafeReader Class"""

# Standard library imports
from pathlib import Path

# Third party imports
import pandas as pd

# Local application imports
from data_reporter.data.config import FACT_TABLE_PATH
from file_reader import readers
from file_reader.safe_reader import SafeReader


def test_SafeReader():

    with SafeReader(FACT_TABLE_PATH) as sr:
        assert len(sr.data) > 0

    # should fail since xlsm is not valid
    # with SafeReader("my/path.xlsm") as sr:
    #     pass
    
    assert not Path(sr.temp_dir).exists()

    


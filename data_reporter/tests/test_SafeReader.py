from file_reader import readers
from file_reader.safe_reader import SafeReader
from data.config import FACT_TABLE_PATH
import pandas as pd
from pathlib import Path

def test_SafeReader():

    with SafeReader(FACT_TABLE_PATH) as sr:
        assert len(sr.data) > 0

    # should fail since xlsm is not valid
    # with SafeReader("my/path.xlsm") as sr:
    #     pass
    
    assert not Path(sr.temp_dir).exists()

    


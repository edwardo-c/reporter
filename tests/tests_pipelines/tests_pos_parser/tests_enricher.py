from pipelines.pos_parser.enrichment.enricher import Enricher
import pytest
import pandas as pd

@pytest.fixture
def valid_enricher():

    period_date = "10/31/2025"
    cat_cfg = {
        "left": "part_number",
        "right": "category",
        "mapping": {
            "part_1" : "cat_1",
            "PART_2" : "CAT_2",
            "part_3   " : "cat_3   ",
        }
    }
    # three white spaces after part_3 and cat_3

    return Enricher(
        period_date=period_date,
        category_cfg=cat_cfg,
        credit_cfg = None
    )

def test_enricher_fixture(valid_enricher):
    assert valid_enricher.period_date == pd.to_datetime("10/31/2025", errors="coerce")
    assert valid_enricher.category_cfg["mapping"] == {"PART_1" : "CAT_1", "PART_2" : "CAT_2", "PART_3" : "CAT_3"}

def test_invalid_enricher():
    
    period_date = "10/31/2025"

    with pytest.raises(ValueError):

        invalid_cat_cfg = {
            "not_left": "part_number",
            "not_right": "category",
            "not_mapping": {"part_1" : "cat_1"}
        }
        
        Enricher(
            period_date=period_date,
            category_cfg=invalid_cat_cfg,
            credit_cfg=None
        )
    

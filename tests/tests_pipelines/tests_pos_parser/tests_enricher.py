from pipelines.pos_parser.enrichment.enricher import Enricher
import pytest
import pandas as pd

@pytest.fixture
def enricher():

    period_date = "10/31/2025"
    cat_cfg = {
        "left": "part_number",
        "right": "category",
        "mapping": {
            "part_1" : "cat_1",
            "PART_2" : "CAT_2",
            "part_3" : "cat_3",
        }
    }
    
    credit_cfg = {
        "out": "SalesRep",
        "rules": [
            {
                "mode": "dynamic",
                "left": "distributor",
                "mapping": {"foo": "bar", "coco": "butter"},
            },
            {
                "mode": "dynamic",
                "left": "buyer_name",
                "mapping": {"gentle": "art"}
            }
        ]
    }

    return Enricher(
        period_date=period_date,
        category_cfg=cat_cfg,
        credit_cfg=credit_cfg
    )

@pytest.fixture
def data():
    return pd.DataFrame(
        {
            "part_number" : ["part_1", "PART_2", "pART_3"]
        }
    )

@pytest.fixture
def credit_data():
    return pd.DataFrame({
        "distributor": ["foo", "coco", "sub"],
        "buyer_name": [None, None, "gentle"],
        "customer_name": ["fish", "ham", "single"],
        "bill_to_state": ["IL", "FL", "MN"],
        "ship_to_state": ["CA", "NY", "AZ"],
        "ship_to_zip": [90210, 10001, 85201],
        "part_number": ["part_1", "part_2", "part_3"],
    })

def test_enricher_fixture(enricher):
    assert enricher.period_date == pd.to_datetime("10/31/2025", errors="coerce")
    assert enricher.category_cfg["mapping"] == {"PART_1" : "CAT_1", "PART_2" : "CAT_2", "PART_3" : "CAT_3"}

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
    
def test_add_category(enricher, data):
    expected = pd.DataFrame(
        {
            "part_number": ["part_1", "PART_2", "pART_3"],
            "category": ["CAT_1", "CAT_2", "CAT_3"],
        }
    )

    result = enricher.add_category(data)
    pd.testing.assert_frame_equal(result, expected)

def test_dynamic_credit(enricher, credit_data):
    df = credit_data.copy()

    result = enricher.add_credit(df)

    expected_sales_rep = pd.Series(
        ["bar", "butter", "art"], 
        index=result.index, 
        name="SalesRep",
        dtype="object",
    )

    pd.testing.assert_series_equal(result["SalesRep"], expected_sales_rep)

    
import pytest
import pandas as pd
from pipelines.pos_parser.enrichment.credit_adapters.credit_maps import load_map

# tests/conftest.py
import pandas as pd
import pytest

# tests/conftest.py
import pandas as pd
import pytest

@pytest.fixture
def temp_excel_map_horizontal(tmp_path):
    """
    Creates a temporary Excel file with two horizontal 2-column mapping tables
    on the same worksheet. Headers start on Excel row 3.
    - Table 1: columns A:B  -> indices 0,1
    - Table 2: columns D:E  -> indices 3,4
    """

    table1 = pd.DataFrame({
        "Key1": ["a", "b", "c"],
        "Value1": ["x", "y", "z"],
    })

    table2 = pd.DataFrame({
        "Key2": ["foo", "bar"],
        "Value2": ["alpha", "beta"],
    })

    file_path = tmp_path / "test_maps.xlsx"

    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        # Header on Excel row 3 → startrow=2 (0-based)
        table1.to_excel(
            writer,
            sheet_name="Config",
            index=False,
            startrow=2,   # row 3
            startcol=0,   # A
        )

        table2.to_excel(
            writer,
            sheet_name="Config",
            index=False,
            startrow=2,   # row 3
            startcol=3,   # D
        )

    return file_path


def test_load_map_table1(temp_excel_map_horizontal):
    result = load_map(
        path=temp_excel_map_horizontal,
        sheet="Config",
        usecols=[0, 1],   # A, B
        skiprows=2,       # header on Excel row 3
    )

    assert result == {"a": "x", "b": "y", "c": "z"}


def test_load_map_table2(temp_excel_map_horizontal):
    result = load_map(
        path=temp_excel_map_horizontal,
        sheet="Config",
        usecols=[3, 4],   # D, E
        skiprows=2,
    )

    assert result == {"foo": "alpha", "bar": "beta"}


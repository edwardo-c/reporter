from typing import Any, Mapping


def count_by_col_index(col_index: int, payload) -> dict[Any, int]:
    # used when grouping does not exist - still being tested
    d = {}
    for r in payload['factMap']['T!T']['rows']:
        row_value = (r["dataCells"][col_index]['label'])
        if row_value in d:
            d[row_value] = d[row_value] + 1
        else:
            d[row_value] = 1
    return d



"""
used when grouping exists

exepcted result: Mapping[str, int] = {
    'ec@email.com': 10, 
}
"""

def get_grouped_row_count(payload: Mapping[Any, Any]):
    """get group value and row count for group"""
    pass
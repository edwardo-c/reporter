from typing import Any

def count_by_col_index(col_index: int, payload) -> dict[Any, int]:
    d = {}
    for r in payload['factMap']['T!T']['rows']:
        row_value = (r["dataCells"][col_index]['label'])
        if row_value in d:
            d[row_value] = d[row_value] + 1
        else:
            d[row_value] = 1
    return d
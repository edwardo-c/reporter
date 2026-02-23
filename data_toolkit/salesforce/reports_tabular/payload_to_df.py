import pandas as pd

def payload_to_df(payload):
    rows = payload["factMap"]['T!T']['rows']
    cols = payload["reportMetadata"]["detailColumns"]
    result = []
    for row in rows:
        cells = row["dataCells"]
        row_dict = {}

        if len(cols) != len(cells):
            raise ValueError(
                f"Rows and Columns from payload must be the same length."
            )

        for col, cell in zip(cols, cells):
            row_dict[col] = cell.get("label", "value")
        result.append(row_dict)

    return pd.DataFrame(result)
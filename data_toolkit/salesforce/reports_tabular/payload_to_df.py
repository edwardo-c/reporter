import pandas as pd

def payload_to_df(
        payload,
        human_readable: bool = False
    ):
    """
    
    """
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
            
            if human_readable:
                row_dict[col] = cell["label"]
            else:
                row_dict[col] = cell["value"]
            
        result.append(row_dict)

    return pd.DataFrame(result)
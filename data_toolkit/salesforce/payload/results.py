import pandas as pd

def build_failed_df(results, payload):
    failed_rows = []

    for i, result in enumerate(results):
        if not result["success"]:
            row = payload[i].copy()
            row["error"] = result["errors"]
            failed_rows.append(row)

    return pd.DataFrame(failed_rows)
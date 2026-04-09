import pandas as pd

def get_mapping(
        df: pd.DataFrame,
        key_col: str,
        values_col: str
    ) -> dict[str, list[str]]:
    """
    converts a dataframe to {identifier: ['values', 'in', 'group'],}
    
    Raises on columns not found in dataframe

    Assumes data has been cleaned and datatypes managed upstream

    """
    existing_cols = list(df.columns)

    if key_col not in existing_cols:
        raise ValueError(f"key column: {key_col} not in dataframe")
    elif values_col not in existing_cols:
        raise ValueError(f"value column: {values_col} not in dataframe")

    return (
        df
        .groupby(key_col)[values_col]
        .agg(list)
        .to_dict()
    )




# deprecated

def extract_contacts_from_df(df: pd.DataFrame) -> dict[str, list[str]]:
    """Return {account -> [contacts]} from df."""
    return (
        df.assign(
            **{
                "ACU Customer ID": df["ACU Customer ID"].astype(str).str.strip(),
                "Email": df["Email"].astype(str).str.strip(),
                }
            )
            .groupby("ACU Customer ID", sort=False)["Email"]
            .agg(list)
            .to_dict()
    )
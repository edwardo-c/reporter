import pandas as pd
import numpy as np


def normalize_sales(
    df: pd.DataFrame,
    qty_col: str = "ShipQuantity",
    unit_cost_col: str = "UnitCost",        # may not exist
    is_return_col: str | None = "IsReturn", # may not exist
    ext_col: str = "ExtendedSales",         # vendor ext if present, else we create it
    return_id=None,
) -> pd.DataFrame:
    df = df.copy()

    breakpoint()

    if isinstance(return_id, str):
        return_id = [return_id]

    # ---------- 1) Canonical quantity sign ----------
    qty = df[qty_col].astype(float)

    if (
        is_return_col is not None
        and return_id is not None
        and is_return_col in df.columns
    ):
        mask_return = df[is_return_col] == return_id
        qty = qty.abs()
        qty.loc[mask_return] *= -1

    # write back canonical quantity (overwriting qty_col is fine here)
    df[qty_col] = qty

    # ---------- 2) Choose base extended source (prefer vendor) ----------

    base_ext = None

    # Prefer vendor extended if the column actually exists and has any non-null values
    vendor_has_ext = ext_col in df.columns
    if vendor_has_ext and df[ext_col].notna().any():
        base_ext = df[ext_col].astype(float)

    # Fallback: compute from qty * unit_cost if we don't have usable vendor ext
    elif unit_cost_col in df.columns and df[unit_cost_col].notna().any():
        unit_cost = df[unit_cost_col].astype(float)
        base_ext = qty * unit_cost

    # ---------- 3) Align extended sign with quantity & ensure column exists ----------

    if base_ext is not None:
        # ensure magnitude is from source, sign from qty
        ext = base_ext.abs()
        ext.loc[qty < 0] *= -1
        df[ext_col] = ext
    else:
        # no usable extended source at all → still provide the column
        df[ext_col] = np.nan

    return df


import pandas as pd
import numpy as np


def normalize_sales(
    df: pd.DataFrame,
    src_qty_col: str = "SrcShipQuantity",
    unit_cost_col: str = "UnitCost",          # may not exist
    src_ext_col: str = "SrcExtendedSales",    # may not exist
    is_return_col: str | None = "IsReturn",
    return_id=None,
    ext_out_col: str = "ExtendedSales",
    qty_out_col: str = "ShipQuantity",
) -> pd.DataFrame:
    """
    Normalize quantity and extended sales into canonical columns.

    - SrcShipQuantity: raw vendor quantity
    - ShipQuantity: canonical signed quantity (negative for returns)
    - ExtendedSales: canonical extended amount, computed as:
        * ShipQuantity * UnitCost if UnitCost is available
        * otherwise from SrcExtendedSales, with our own sign logic
    """
    df = df.copy()

    # ---------- 1) Canonical quantity (signed) ----------
    qty = df[src_qty_col].astype(float)

    mask_return = None
    if is_return_col is not None and return_id is not None and is_return_col in df.columns:
        mask_return = df[is_return_col] == return_id
        qty = qty.abs()
        qty.loc[mask_return] *= -1

    df[qty_out_col] = qty

    # ---------- 2) Canonical extended sales ----------
    ext = None

    # Prefer: compute from UnitCost if it exists and has non-null values
    if unit_cost_col is not None and unit_cost_col in df.columns and df[unit_cost_col].notna().any():
        unit_cost = df[unit_cost_col].astype(float)
        ext = qty * unit_cost

    # Fallback: use SrcExtendedSales if UnitCost is missing/useless
    elif src_ext_col is not None and src_ext_col in df.columns:
        ext = df[src_ext_col].astype(float)

        # Apply our sign logic so it matches ShipQuantity
        if mask_return is not None:
            ext = ext.abs()
            ext.loc[mask_return] *= -1

    # If we got an extended series, set it; otherwise create an all-NaN column
    if ext is not None:
        df[ext_out_col] = ext
    else:
        df[ext_out_col] = np.nan

    return df

from pathlib import Path

import pandas as pd

from plan_executor.registry import register_operation
from utils.validators import valid_dir

@register_operation("csv_partitioned")
def export_partitioned_csv(
        df: pd.DataFrame, 
        partition_by: str, 
        root_dir: Path,
        dry_run: bool = False
    ) -> None | list:

    root_dir: Path = valid_dir(root_dir) # validate dir, all raises inside func

    dry_run_list = [] if dry_run else None

    for val, part in df.groupby(by=partition_by, dropna=True):
        export_path = root_dir / f"{val}.csv"
        if dry_run:
            dry_run_list.append(export_path)    
        else:
            part.to_csv(export_path, index=False)

    if dry_run:
        return dry_run_list
    else:
        None


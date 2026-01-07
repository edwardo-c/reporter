import pandas as pd
from pathlib import Path

class PosXref():
    def __init__(
        self,
        left_df: pd.DataFrame,
        right_df: pd.DataFrame,
        join_columns: dict[str: str],
        outgoing_path: str | Path | None
    ):
        """
        args: 
        outgoing_path: appends data to outoing csv (manual xref review)
        """

        self._left_join_cols = list(join_columns.keys())
        self._right_join_cols = list(join_columns.values())

        # right not deduped because it is expected to be a master file; 
        # aka: nothing should be dropped as a part of this additory pipeline
        self.right_df = right_df
        
        self.left_df = left_df
        self._dedup_left()

    def _inner_join(self):
        """
        identifies data in left not in right
        assumes normalized data to allow for pre user defined normalization
        join_columns: column in left(key) that matches from right(value)
        """
        
        left = self.left_df.copy()
        right = self.right_df.copy()

        lc = self._left_join_cols
        rc = self._right_join_cols
        original_left_columns = list(left.columns)

        left_col_count = len(lc)
        right__col_count = len(rc)
        
        if (left_col_count == 1) and (right__col_count == 1):
            
            left_on = lc[0]
            right_on = rc[0]
            
        elif (left_col_count > 1) and (right__col_count > 1):

            left['lkey'] = left[lc].agg("|".join, axis=1)
            right['rkey'] = right[rc].agg("|".join, axis=1)

            left_on = 'lkey'
            right_on = 'rkey'

        result = left.merge(
            right, 
            left_on=left_on, 
            right_on=right_on, 
            how="inner"
        )

        return result[original_left_columns]

    def _dedup_left(self) -> None:
        _df = self.left_df.copy()
        deduped = _df.drop_duplicates(subset=self._left_join_cols, ignore_index=True)
        self.left_df = deduped

    def _append_to_outgoing():
        pass

    def run(self, mode = 'write'):

        pass
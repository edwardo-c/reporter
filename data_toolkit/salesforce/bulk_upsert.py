import pandas as pd
from data_toolkit.cleaners.schema import IntCol, StrCol, DateCol
from simple_salesforce import Salesforce
from data_toolkit.api_serialization import serialize_dataframe_for_api
from data_toolkit.cleaners.schema import enforce_schema


from pathlib import Path

class SFBulkObj:
    def __init__(
            self, 
            object_name: str, 
            external_id: str, 
            df: pd.DataFrame,
            schema: list[IntCol | StrCol | DateCol]
        ):
        self.object_name = object_name
        self.external_id = external_id
        self.df = df
        self.schema = schema
        self.payload = None
        self.upsert_results = None
        self.failed_df = None
        self._schema_enforced = False
        self.has_failed_rows = False

    def _enforce_schema(self) -> None:
        if not self._schema_enforced:
            self.df = enforce_schema(self.schema, self.df)
            self._schema_enforced = True

    def upsert(self, sf: Salesforce) -> list[dict]:
        if self.payload is None: 
            self.build_bulk_payload()
        self.upsert_results = getattr(sf.bulk, self.object_name).upsert(self.payload, self.external_id)
        self.build_failed_df()
        return self.upsert_results

    def build_bulk_payload(self) -> list[dict]:
        if not self._schema_enforced:
            self._enforce_schema()
        _df = serialize_dataframe_for_api(self.df)
        self.payload = _df.to_dict('records')
        return self.payload

    def failed_df_to_csv(self, out_path: str | Path) -> None:
        if self.upsert_results is None:
            raise ValueError("Payload has not been uploaded, no results to parse.")

        if self.failed_df is None:
            self.build_failed_df()

        self.failed_df.to_csv(str(out_path), index=False)

    def build_failed_df(self) -> pd.DataFrame:
        if self.upsert_results is None:
            raise ValueError("Payload has not been uploaded, no results to parse.")
        failed_rows = []
        for i, result in enumerate(self.upsert_results):
            if not result["success"]:
                row = self.payload[i].copy()
                row["error"] = result["errors"]
                failed_rows.append(row)

        self.failed_df = pd.DataFrame(failed_rows)

        if len(self.failed_df) > 0:
            self.has_failed_rows = True

        return self.failed_df
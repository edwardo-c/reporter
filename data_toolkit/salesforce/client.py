from simple_salesforce import Salesforce
import pandas as pd

class SFClient:
    def __init__(
            self, 
            username: str | None = None,
            password: str | None = None,
            security_token: str | None = None,
            sf: Salesforce | None = None
        ):
        
        self._login_args = (username, password, security_token)
        self._sf = sf

        if self._sf is None:
            self._connect()
        else:
            self._sf = sf

    def _connect(self):
        if self._sf is None:
            u, p, t = self._login_args
            self._sf = Salesforce(username=u, password=p, security_token=t)
            self._login_args = (None, None, None)

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc, tb):
        self._sf = None

    def insert_record(self, obj_name: str, data: dict):
        return getattr(self._sf, obj_name).create(data)
    
    def delete_record(self, obj_name: str, id: str):
        return getattr(self._sf, obj_name).delete(id)

    def query(self, soql: str, df: bool = True) -> pd.DataFrame | dict:
        res = self._sf.query_all(soql)
        records = res["records"]
        if df:
            return pd.DataFrame(records).drop(columns=["attributes"], errors="ignore")
        else:
            return records
    
    def get_report(
            self, 
            report_id: str, 
            include_details: bool = True
        ):
        """
        returns the json response body from a predefined salesforce report
        """
        
        if not isinstance(report_id, str):
            raise TypeError(f"report_id must be str, got: {type(report_id)}")
        elif len(report_id) == 0:
            raise ValueError(
                f"report_id cannot be a 0 length string"
                "report_ids are approximatly 13-15 characters,"
                "usually starting with '00O', often found in the URL of the report"
            )


        report_results = self._sf.restful(
            f'analytics/reports/{report_id}?includeDetails={str(include_details)}'
        )
        
        if not bool(report_results["allData"]):
            raise ValueError(
                f"Incomplete data set captured! \n"
                f"Due to pagination, you are not capturing the complete data set \n"
                f"Prefer SFCLient.query(MY_SOQL_STR)"    
            )

        # TODO: log the name of the report found using the metadata

        return report_results
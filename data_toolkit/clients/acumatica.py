import requests
import pandas as pd
import logging


class AcumaticaClient():
    """
    Thin Acumatica Client for returning Odata
    usage:
    ```
    a = AcumaticaClient(username='user', password='pw')
    a.odata_to_json()
    ```
    """
    def __init__(self, username: str, password: str):
        self._session: requests.Session = None
        self.auth: tuple = (username, password)

        self._authenticate()

        username = None
        password = None
        self.auth = (None, None)

    def _authenticate(self):
        s = requests.Session()
        u, p = self.auth
        s.auth = (u, p)
        self._session = s

    def odata(self, url: str, params: dict = {"$format": "json"}, df: bool = False) -> dict | pd.DataFrame:
        """Return odata url as df or dict"""
        fmt = params.get("$format", None)
        j = "json"
        if not fmt or fmt != j:
            params["$format"] = j
            logging.debug("json not set in odata params, auto added")

        resp = self._session.get(url, params=params)
        data = resp.json().get("value", [])

        if not data:
            logging.warning(f"Odata url returned nothing! -- {url}")

        if df:
            return pd.json_normalize(data)
        else:
            return data
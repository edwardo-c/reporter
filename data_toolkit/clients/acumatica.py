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
        self._acu: requests.Session = None
        self.auth: tuple = (username, password)

        self._authenticate()

        username = None
        password = None
        self.auth = (None, None)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self._acu = None

    def _authenticate(self):
        s = requests.Session()
        u, p = self.auth
        s.auth = (u, p)
        self._acu = s

    def odata(self, url: str, params: dict | None = None, df: bool = False):
        params = params or {}
        params.setdefault("$format", "json")

        resp = self._acu.get(url, params=params)

        try:
            payload = resp.json()
        except ValueError:
            logging.error(f"Non-JSON response from Acumatica: {resp.text[:200]}")
            raise

        data = payload.get("value", [])

        if not data:
            logging.warning(f"Odata url returned nothing! -- {url}")

        return pd.json_normalize(data) if df else data

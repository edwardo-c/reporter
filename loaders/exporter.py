# standard library imports

# third party imports
import pandas as pd

# internal application imports
from loaders.registry import EXPORT_REGISTRY

class DataExporter():
    def __init__(self, data: pd.DataFrame, cfg: dict):
        self.cfg = cfg
        self.data: pd.DataFrame = data
        self.registry = EXPORT_REGISTRY

    def export(self):
        func = self.registry[self.cfg['op']]
        func(self.data, self.cfg)

    # TODO: add error checking for proper data types
        
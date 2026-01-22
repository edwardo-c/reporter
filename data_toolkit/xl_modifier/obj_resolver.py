import xlwings as xw
from data_toolkit.xl_modifier.obj_dataclasses import TableRef

class ObjectResolver():
    def __init__(self, wb: xw.Book):
        self.wb = wb
        self._cache = {}

    def resolve(self, obj_address: dict | None = None):
        """
        returns the xlwings object based off the heirarchical object address
        e.g: list object = sheet + table name; etc
        """

        if isinstance(obj_address, TableRef):
            obj = self.wb.sheets[obj_address.sheet].tables[obj_address.table]
            return obj
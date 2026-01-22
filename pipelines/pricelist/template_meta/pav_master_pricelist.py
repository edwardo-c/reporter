from dataclasses import dataclass, field
from data_toolkit.xl_modifier.obj_dataclasses import TableRef


@dataclass(frozen=True)
class MasterPriceListTemplateMeta():
    master_table: TableRef = TableRef(sheet="Price List", table="MasterPriceList")
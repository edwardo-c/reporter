from dataclasses import dataclass
from typing import Optional, Dict

from data_toolkit.cleaners.adapters import CanonicalSchemaDef

@dataclass
class PosSchemaMapping:
    """
    Per-source mapping: canonical_field -> source column name or None.
    This matches cfg["CanonicalSchema"] from YAML.
    """
    PiiPartNumber: Optional[str] = None
    ShipQuantity: Optional[str] = None
    ExtendedSales: Optional[str] = None
    SoldToName: Optional[str] = None
    SaleDate: Optional[str] = None
    BillToCustomerZip: Optional[str] = None
    BillToCustomerState: Optional[str] = None
    ShipToState: Optional[str] = None
    ShipToZip: Optional[str] = None

    def as_dict(self) -> Dict[str, Optional[str]]:
        return self.__dict__.copy()

POS_SCHEMA_DEF = CanonicalSchemaDef(
    str_fields=(
        "SoldToName",
        "PiiPartNumber",
        "BillToCustomerZip",
        "BillToCustomerState",
        "ShipToState",
        "ShipToZip",
    ),
    float_fields=("ShipQuantity", "ExtendedSales"),
    date_fields=("SaleDate",),
    zipcode_fields=("ShipToZip", "BillToCustomerZip"),
)


from dataclasses import dataclass
from typing import Optional, Dict

from data_toolkit.cleaners.adapters import CanonicalSchemaDef

@dataclass
class PosSchemaMapping:
    """
    Per-source mapping: canonical_field -> source column name or None.
    This matches cfg["CanonicalSchema"] from YAML.
    """
    SoldToName: Optional[str] = None
    SaleDate: Optional[str] = None
    PiiPartNumber: Optional[str] = None
    IsReturn: Optional[str] = None
    ShipQuantity: Optional[str] = None
    UnitCost: Optional[str] = None
    ExtendedSales: Optional[str] = None
    BillToCustomerZip: Optional[str] = None
    BillToCustomerState: Optional[str] = None
    ShipToState: Optional[str] = None
    ShipToZip: Optional[str] = None
    BuyerName: Optional[str] = None

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
        "BuyerName",
        "IsReturn",
    ),
    float_fields=("ShipQuantity", "ExtendedSales", "UnitCost"),
    date_fields=("SaleDate",),
    zipcode_fields=("ShipToZip", "BillToCustomerZip"),
    null_subset_fields=(
        "SoldToName", 
        "PiiPartNumber", 
        "BillToCustomerZip", 
        "BillToCustomerState", 
        "ShipToState",
        "ShipToZip"
    ),
)


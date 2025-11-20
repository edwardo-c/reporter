from dataclasses import dataclass
from typing import Optional, Dict
from data_toolkit.cleaners.adapters import CanonicalSchemaDef

@dataclass
class CanonicalSchemaMapping:
    """
    Per-source mapping:
    canonical_field -> source column name (or None if missing).
    """
    SoldToName: Optional[str] = None
    SaleDate: Optional[str] = None
    PiiPartNumber: Optional[str] = None
    ShipQuantity: Optional[str] = None
    ExtendedSales: Optional[str] = None
    BillToCustomerZip: Optional[str] = None
    BillToCustomerState: Optional[str] = None
    ShipToState: Optional[str] = None
    ShipToZip: Optional[str] = None

    def as_dict(self) -> Dict[str, Optional[str]]:
        # canonical_name -> source_column or None
        return self.__dict__.copy()

POS_SCHEMA_DEF = CanonicalSchemaDef(
    str_fields=(
        "SoldToName", "PiiPartNumber", "BillToCustomerZip", 
        "BillToCustomerState", "ShipToState", "ShipToZip",), 
    float_fields=("ShipQuantity", "ExtendedSales"), 
    date_fields=("SaleDate",), 
    zipcode_fields=("ShipToZip", "BillToCustomerZip"), 
)
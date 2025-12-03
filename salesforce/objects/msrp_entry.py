from dataclasses import dataclass, field

from salesforce.ids.registry import MSRP_ID

def bulk_arrange_msrp(
        parts_to_organize: set[str], 
        data_dict: dict[str, dict], 
        *,
        msrp_price_key: str = "MSRP",
        sf_id_key: str = "sf_id",
        ) -> list:
    
    """organizes parts as NewPart (dataclass) using data_dict"""

    msrp_entries = []

    for part in parts_to_organize:

        part_data_dict = data_dict[part]

        if part_data_dict:

            price = part_data_dict.get(msrp_price_key, None)
            sf_id = part_data_dict.get(sf_id_key, None)
            product = part

            msrp_entries.append(
                MSRPEntry(
                    price=price,
                    id=sf_id,
                    product=product
                ))

        else:
            # intentional skip
            continue
    
    return msrp_entries

@dataclass
class MSRPEntry:
    """
    Required params for an msrp entry in Salesforce
    usage: 
    ```
    import simple_salesforce as sf
    sf.PricebookEntry.create(MSRPEntry.params)
    ```
    """
    price: float
    id: str = field(repr=False)
    product: str | None = field(default=None)
    params: dict[str, str | bool] = field(default_factory=dict, repr=False)
    valid: bool = field(default=True)

    def __post_init__(self):
        
        if not self.id:
            self.valid = False

        if not self.product:
            self.product = self.id

        if not self.params:
            self.params = {
                "IsActive": True,
                "CurrencyIsoCode": "USD",
                "Pricebook2Id": MSRP_ID,
                "UnitPrice": self.price,
                "Product2Id": self.id
            }

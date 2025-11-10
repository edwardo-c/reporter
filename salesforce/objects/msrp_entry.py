from dataclasses import dataclass, field

from salesforce.ids.registry import MSRP_ID

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

    def __post_init__(self):
        
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

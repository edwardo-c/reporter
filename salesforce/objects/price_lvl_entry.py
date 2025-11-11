# load id cfg
# store id cfg
# expose for use in entries


from dataclasses import dataclass, field

from salesforce.ids.registry import PRICE_LVL_IDS

@dataclass
class PriceLvlEntry:
    """
    Required params for an price list entry in Salesforce
    usage: 
    ```
    import simple_salesforce as sf
    sf.Price_List_Entry__c.create(PriceLvlEntry.params)
    ```
    """
    price: float
    id: str = field(repr=False)
    product: str | None = field(default=None)
    price_list_id: str | None = field(repr=False, default=None)
    params: dict[str, str | bool] = field(default_factory=dict, repr=False)
    valid: bool = field(default=True)

    def __post_init__(self):
        
        if self.product is None:
            self.product = self.id

        if not self.price_list_id is None:
            id = ...

        if not self.params:
            self.params = {
                "Active__c": True,
                "CurrencyIsoCode": "USD",
                "Price_List__c": "Price List ID Here",
                "Price_List_Price__c": self.price,
                "Product__c": self.id
            }

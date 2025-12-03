# load id cfg
# store id cfg
# expose for use in entries


from dataclasses import dataclass, field

from salesforce.ids.registry import PRICE_LVL_IDS

def bulk_arrange_price_lvls(
        parts_to_organize: set[str], 
        data_dict: dict[str, dict], 
        *,
        price_keys: set = ("dealer", "partner", "distributor", "special"),
        sf_id_key: str = "sf_id",
        price_group_key: str | None = "pricegroup",
        ) -> list:
    
    """organizes parts as NewPart (dataclass) using data_dict"""

    price_lvl_entries = []

    norm_data_dict = {
        part: {k.casefold(): v for k, v in part_dict.items()}
        for part, part_dict in data_dict.items()
    }

    for part in parts_to_organize:

        part_data_dict = norm_data_dict[part]

        if part_data_dict:

            part_number = part
            part_sf_id = part_data_dict.get(sf_id_key, None)
            price_group = part_data_dict.get(price_group_key, None)
            
            for price_key in price_keys:

                price = part_data_dict.get(price_key, None)

                price_lvl_entries.append(
                    PriceLvlEntry(
                        price=price,
                        part_number=part_number,
                        part_sf_id=part_sf_id,
                        price_group=price_group,
                        price_lvl=price_key
                    )
                )
        else:
            # intentional skip
            continue
    
    return price_lvl_entries


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
    price_group: str | None
    part_sf_id: str = field(repr=False)
    part_number: str | None = field(default=None)
    price_lvl: str | None = field(default=None)
    price_list_id: str | None = field(repr=False, default=None)
    params: dict[str, str | bool] = field(default_factory=dict, repr=False)
    valid: bool = field(default=True)

    def __post_init__(self):
        
        if self.part_number is None:
            self.part_number = self.part_sf_id

        # try finding an id if one was not provided
        if self.price_list_id is None:
            
            pg = self.price_group
            
            if pg and isinstance(pg, str):
                pg = pg.casefold()
                
                pl_ids = PRICE_LVL_IDS.get(pg, None)
                pl_id = pl_ids.get(self.price_lvl, None)
        
                if pl_id:
                    self.price_list_id = pl_id
                else:
                    self.valid = False
            else:
                # intentional skip
                self.valid = False

        if not self.params:
            self.params = {
                "Active__c": True,
                "CurrencyIsoCode": "USD",
                "Price_List__c": self.price_list_id,
                "Price_List_Price__c": self.price,
                "Product__c": self.part_sf_id
            }

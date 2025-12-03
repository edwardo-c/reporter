from dataclasses import dataclass, field

from salesforce.ids.registry import price_grp_id

def bulk_arrange(
        parts_to_organize: set[str], 
        data_dict: dict[str, dict], 
        *,
        category_key: str = "Category",
        status_key: str = "ItemStatus",
        pmplcm_key: str = "ProductLifeCycleManagement",
        map_price_key: str = "USDMAPPrice",
        description_key: str = "Description",
        price_group_key: str = "PriceGroup"
        ) -> list:

    """organizes parts as NewPart (dataclass) using data_dict"""

    auth_req_options = set((None, 0, "0", ""))

    new_parts = []

    for part in parts_to_organize:

        part_data_dict = data_dict[part]

        if part_data_dict:
            
            
            name = part
            category = part_data_dict.get(category_key, None)
            status = part_data_dict.get(status_key, None)
            pmplcm = part_data_dict.get(pmplcm_key, None)
            map_price = part_data_dict.get(map_price_key, None)
            auth_req = (False if map_price in auth_req_options else True)
            desc = part_data_dict.get(description_key, None)
            pg = part_data_dict.get(price_group_key, None)

            new_parts.append(
                NewPart(
                    name=name,
                    category=category,
                    acu_status=status,
                    acu_pmplcm=pmplcm,
                    acu_auth_required=auth_req,
                    description=desc,
                    price_group=pg
            ))

        else:
            # intentional skip
            continue
    
    return new_parts

@dataclass
class NewPart:
    """
    Required params for a new part in Salesforce
    usage: 
    ```
    import simple_salesforce as sf
    sf.Product2.create(NewPart.params)
    ```
    valid 
      categories:
          MOUNT, DVLED, TV, KIOSK
      
      price_group:  
          "CORE", "ET", "DS", "DVLED", 
          "KIOSK", "NEPTUNE", "HOSP", "E-TAIL", "RETAIL"
    """
    name: str
    category: str
    acu_status: str = field(repr=False)
    acu_pmplcm: str = field(repr=False)
    acu_auth_required: bool = field(repr=False)
    description: str = field(repr=False)
    price_group: str | None = field(default=None)
    price_group_id: str | None = field(default=None)
    CurrencyIsoCode: str = field(default="USD", repr=False)
    IsActive: bool = field(default=True, repr=False)
    editable: bool = field(default=True, repr=False)

    params: dict[str, str | bool] | None = field(default_factory=dict, repr=False)
    valid: bool = field(default=True, repr=False)
    
    def __post_init__(self):

        pg_id = self.price_group_id

        if not pg_id:
            pg_id = price_grp_id(self.price_group)
            if not pg_id:
                self.valid = False
                return

        self.params = {
                "Name": self.name,
                "Part_Number__c": self.name,
                "ProductCode": self.name,
                "Category__c": self.category,
                "Description": self.description,
                "Price_Group__c": pg_id,
                "CurrencyIsoCode": self.CurrencyIsoCode,
                "IsActive": self.IsActive, 
                "SBQQ__QuantityEditable__c": self.editable,
                "ACU_Item_Status__c": self.acu_status,
                "ACU_PMPLCM__c": self.acu_pmplcm,
                "ACU_Authorization_Required__c": self.acu_auth_required
            }
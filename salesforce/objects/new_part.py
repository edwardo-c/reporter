from dataclasses import dataclass, field

from salesforce.ids.registry import price_grp_id

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
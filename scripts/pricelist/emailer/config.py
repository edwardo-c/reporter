from enum import Enum

from data_toolkit.readers.sources import SFQuery, OData
from dataclasses import dataclass

from scripts.pricelist.emailer import SOQL
from data_toolkit.cleaners.schema import StrCol

class LoadersSchema(Enum):
    email = "email"
    acu_id = "acu_id"
    cust_name = "cust_name"

# ================= config for loaders =================
@dataclass(slots=True, frozen=True)
class MapPair:
    value_col: str
    key_col: str = LoadersSchema.acu_id.value

@dataclass(frozen=True)
class PriceListQuery:
    query: SFQuery | OData
    schema: list[StrCol] | None
    rename_map: dict[str: str] | None
    mapping: MapPair

@dataclass
class Sources:
    sf_internal_query: PriceListQuery
    sf_external_query: PriceListQuery
    acu_customers_query: PriceListQuery

SOURCES = Sources(
    sf_external_query=PriceListQuery(
        query=SFQuery(
            soql=SOQL.EXTERNAL_CONTACTS_SOQL, 
            df_id="external"
        ),
        schema=[
            StrCol("Account.ACU_CUSTOMER_ID__c"),
            StrCol("Email")
        ],
        rename_map={
            "Account.ACU_CUSTOMER_ID__c": LoadersSchema.acu_id.value,
            "Email": LoadersSchema.email.value,
        },
        mapping=MapPair(
            value_col=LoadersSchema.email.value
        )
    ),
    sf_internal_query=PriceListQuery(
        query=SFQuery(
            soql=SOQL.INTERNAL_CONTACTS_SOQL, 
            df_id="internal"
        ),
        schema=[
            StrCol("ACU_CUSTOMER_ID__c"), 
            StrCol("Price_List_Delivery_to_Salesperson__r.Email")
        ],
        rename_map={
            "ACU_CUSTOMER_ID__c": LoadersSchema.acu_id.value,
            "Price_List_Delivery_to_Salesperson__r.Email": LoadersSchema.email.value 
        },
        mapping=MapPair(
            value_col=LoadersSchema.email.value
        )
    ),
    acu_customers_query=PriceListQuery(
        query=OData(
            params={"$select": "CustomerID,CustomerName"},
            url="https://peerless-av.acumatica.com/OData/Peerless-AV/Sales%20Opps%20Customer%20Review",
            df_id="acu_customers"
        ),
        schema=[StrCol("CustomerID"), StrCol("CustomerName")],
        rename_map={
            "CustomerID":LoadersSchema.acu_id.value,
            "CustomerName":LoadersSchema.cust_name.value
        },
        mapping=MapPair(
            value_col=LoadersSchema.email.value
        )
    )
)

RESULTS_LOG = {
    "acu_id": [],
    "pav_created": [],
    "nep_created": [],
    "contacts": []
}
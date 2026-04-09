from enum import Enum

from data_toolkit.readers.sources import SFQuery, OData
from dataclasses import dataclass

from data_toolkit.readers.context import SFCred, AcuCred

from scripts.pricelist.emailer import SOQL
from data_toolkit.cleaners.schema import StrCol


SF_CRED = SFCred(
    username="SF_USER",
    password="SF_PW",
    token="SF_TOKEN"
)

ACU_CRED = AcuCred(
    username="ACU_USERNAME",
    password="ACU_PW"
)

# ================= config for loaders =================

@dataclass(frozen=True)
class PriceListQuery:
    query: SFQuery | OData
    schema: list[StrCol] | None
    rename_map: dict[str: str] | None

class LoadersSchema(Enum):
    email = "email"
    acu_id = "acu_id"
    cust_name = "cust_name"

INTERNAL_CONTACTS_QUERY = PriceListQuery(
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
    }
)

EXTERNAL_CONTACTS_QUERY = PriceListQuery(
    query=SFQuery(
        soql=SOQL.EXTERNAL_CONTACTS_SOQL, 
        df_id="external"
    ),
    schema=[
        StrCol("Email"), 
        StrCol("Account.ACU_CUSTOMER_ID__c")
    ],
    rename_map={
        "Email": LoadersSchema.email.value,
        "Account.ACU_CUSTOMER_ID__c": LoadersSchema.acu_id.value 
    }
)

CUSTOMERS_ODATA = PriceListQuery(
    query=OData(
        params={"$select": "CustomerID,CustomerName"},
        url="https://peerless-av.acumatica.com/OData/Peerless-AV/Sales%20Opps%20Customer%20Review",
        df_id="acu_customers"
    ),
    schema=[StrCol("CustomerID"), StrCol("CustomerName")],
    rename_map={
        "CustomerID":LoadersSchema.acu_id.value,
        "CustomerName":LoadersSchema.cust_name.value
    }
)


# ================ config for attachment maps ==========
ACU_ID_RE = r"[A-Za-z0-9]{1,3}[0-9]{6}"
GLOB_PATTERN = "*.xlsx"

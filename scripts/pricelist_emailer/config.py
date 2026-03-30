from data_toolkit.readers.sources import SFQuery
from dataclasses import dataclass

from data_toolkit.salesforce.client import SFCred
from data_toolkit.attachments.mapper import AttachmentMapCfg

from scripts.pricelist_emailer import SOQL
from data_toolkit.cleaners.df_dtypes.dtype import StrCol


SF_CRED = SFCred(
    username="SF_USER",
    password="SF_PW",
    token="SF_TOKEN"
)

ACU_ID_RE = r"[A-Za-z0-9]{1,3}[0-9]{6}"

NEP_ATTACHMENT_MAP_CFG = AttachmentMapCfg(
    map_id="Neptune",
    src_dir="NEP_FINISHED_LISTS_DIR",
    glob_pattern="*.xlsx",
    re_pattern=ACU_ID_RE
)

PAV_ATTACHMENT_MAP_CFG = AttachmentMapCfg(
    map_id="Peerless-AV",
    src_dir="PAV_FINISHED_LISTS_DIR",
    glob_pattern="*.xlsx",
    re_pattern=ACU_ID_RE
)

@dataclass(frozen=True)
class PriceListSFQuery:
    query: SFQuery
    schema: list[StrCol]

@dataclass
class PriceListSFQueries:
    external: PriceListSFQuery
    internal: PriceListSFQuery

SF_QUERY_OBJS = PriceListSFQueries(
    external=PriceListSFQuery(
        query=SFQuery(soql=SOQL.EXTERNAL_CONTACTS_SOQL, df_id="external"),
        schema=list[
            StrCol("Email"), 
            StrCol("Account.ACU_CUSTOMER_ID__c")
        ]
    ),
    internal=PriceListSFQuery(
        query=SFQuery(soql=SOQL.INTERNAL_CONTACTS_SOQL, df_id="internal"),
        schema=list[
            StrCol("test"), 
            StrCol("test_two")
        ]
    )    
)
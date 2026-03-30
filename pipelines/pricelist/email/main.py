"""Primary runner for emailing finished price lists to customers"""

# standard imports
from dotenv import load_dotenv
import logging
from pathlib import Path
import sys

# third party imports
import pandas as pd

# internal imports
from config.paths import PRICE_LIST_ENV, PRICE_LIST_EMAILER_CFG
from utils.yaml_loader import load_yaml
from data_toolkit.attachments.acu_id import id_to_path_map
from data_toolkit.salesforce.client import SFClient
from pipelines.pricelist.email.bodies import external_email, internal_email, external_boilerplate_email
from data_toolkit.clients.outlook.outlook_sender import BaseEmail, OutlookSender
from pipelines.pricelist.email.recipient_log_enums import RecipientLogSchema as RLS
from pipelines.pricelist.email.recipient_log_enums import RecipientLogSentToVals as RLS_SentToVals
from pipelines.pricelist.email.recipient_log_enums import RecipientLogNone as RLS_NA
from data_toolkit.clients.outlook.outlook import OLClient
from data_toolkit.clients.acumatica import AcumaticaClient

from collections import defaultdict

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format= "%(message)s")

"""
Send Emails = (DRY_RUN = False) and (PROD = True)
"""

DRY_RUN = False # True = exit after send log creation, no emails sent
PROD = True # False = breakpoint at send email to inspect email
RUN_ID = "March_2026"

def main():

    logger.info("Starting Emailer")

    load_dotenv(PRICE_LIST_ENV)

    cfg = load_yaml(PRICE_LIST_EMAILER_CFG)

    sf = SFClient(**cfg["salesforce"]["auth"])

    # =========== External Resources ==============

    pav_attachments = id_to_path_map(Path(cfg["attachments"]["Peerless-AV"]))
    nep_attachments = id_to_path_map(Path(cfg["attachments"]["Neptune"]))

    raw_external_contacts = sf.query(cfg["salesforce"]["data"]["external"]["soql"], df=False)

    external_contacts_cache = defaultdict(list)

    for r in raw_external_contacts:
        external_contacts_cache[r['Account']['ACU_CUSTOMER_ID__c'].strip()].append(r['Email'].strip())

    # ========= Internal Resources ============

    raw_internal_contacts = sf.query(cfg["salesforce"]["data"]["internal"]["soql"], df=False)

    internal_contacts_cache = defaultdict(list)

    for r in raw_internal_contacts:
        customer_id = r["ACU_CUSTOMER_ID__c"].strip()
        email = r["Price_List_Delivery_to_Salesperson__r"]["Email"].strip()

        internal_contacts_cache[customer_id].append(email)

    customer_names = AcumaticaClient(
        **cfg["acumatica"]["auth"]
        ).odata(**cfg["acumatica"]["customers"], df=True)

    customer_names.columns = ["key", "value"]

    # Drop empty key rows (avoids {nan: nan})
    customer_names = customer_names.dropna(subset=["key"])
    customer_names = customer_names.set_index("key")["value"].to_dict()

    # used for placing customer name in internal emails
    cust_name_map = {k.strip(): v.strip().title() for k, v in customer_names.items()}

    # ============== Build Email Log ======================

    pav_accts = set(pav_attachments.keys())
    nep_accts = set(nep_attachments.keys())
    all_accts = sorted(pav_accts.union(nep_accts))

    has_pav = []
    has_nep = []
    ext_contacts = []
    int_contacts = []
    sent_to = []

    for a in all_accts:
        
        has_pav.append(a in pav_accts)
        has_nep.append(a in nep_accts)
        
        ec = external_contacts_cache.get(a, RLS_NA.NA.value)
        ic = internal_contacts_cache.get(a, RLS_NA.NA.value)

        if ic != RLS_NA.NA.value:
            to = RLS_SentToVals.INT.value

        elif ec != RLS_NA.NA.value:
            to = RLS_SentToVals.EXT.value

        else:
            to = RLS_SentToVals.NA.value

        ext_contacts.append(ec)
        int_contacts.append(ic)
        sent_to.append(to)

    recipient_log = pd.DataFrame(
        {
            RLS.ACCT.value   : all_accts,
            RLS.PAV.value    : has_pav,
            RLS.NEP.value    : has_nep,
            RLS.EXT.value    : ext_contacts,
            RLS.INT.value    : int_contacts,
            RLS.SENT_TO.value: sent_to
        }
    )
    
    recipient_log_out_dir = Path(cfg["recipient_log_out_dir"])
    recipient_log_out_path = recipient_log_out_dir /f"Recipient_Log_{RUN_ID}.csv" 
    recipient_log.to_csv(recipient_log_out_path, index=False)

    if DRY_RUN:
        logger.info(f"Dry run complete, results: {recipient_log_out_path}")
        sys.exit()

    # ============== Build Emails ======================
    with OLClient() as ol_app:
        pav_emails = [
            BaseEmail(
                recipients=recipients,
                subject=f"Peerless-AV Monthly Price List - {acct}",
                body=external_boilerplate_email(brand="Peerless-AV"),
                attachments=attachments
            )
            for acct, recipients in external_contacts_cache.items()
            if (attachments:= pav_attachments.get(acct, None))
        ]

        nep_emails = [
            BaseEmail(
                recipients=recipients,
                subject=f"Neptune Monthly Price List - {acct}",
                body=external_boilerplate_email("Neptune"),
                attachments=attachments
            )
            for acct, recipients in external_contacts_cache.items()
            if (attachments:= nep_attachments.get(acct, None))
        ]

        internal_pav_emails = [
            BaseEmail(
                recipients=recipient,
                subject=f"Peerless-AV Monthly Price List - Not Distributed: {acct} - {name}",
                body=internal_email(name),
            )
            for acct, recipient in internal_contacts_cache.items()
            if (name:= cust_name_map.get(acct, None))
        ]

        internal_nep_emails = [
            BaseEmail(
                recipients=recipient,
                subject=f"Neptune Monthly Price List - Not Distributed: {acct} - {name}",
                body=internal_email(name)
            )
            for acct, recipient in internal_contacts_cache.items()
            if (name:= cust_name_map.get(acct, None))
        ]

        # ============ HOT LOOP! Send Emails =======================

        emails = [*pav_emails, *nep_emails, *internal_pav_emails, *internal_nep_emails]
        # used in testing specific emails
        # emails = [*pav_emails]

        for e in emails:
            OutlookSender(
                ol_app=ol_app,
                sent_on_behalf="sales@peerless-av.com",
                prod=PROD
            ).send(e)

    logger.info("All emails sent to outlook client - see outlook")
# ========== bad design due to time constraints, refactor after run ==========

def extract_contacts_from_df(df: pd.DataFrame) -> dict[str, list[str]]:
    """Return {account -> [contacts]} from df."""
    return (
        df.assign(
            **{
                "ACU Customer ID": df["ACU Customer ID"].astype(str).str.strip(),
                "Email": df["Email"].astype(str).str.strip(),
                }
            )
            .groupby("ACU Customer ID", sort=False)["Email"]
            .agg(list)
            .to_dict()
    )

if __name__ == "__main__":
    main()


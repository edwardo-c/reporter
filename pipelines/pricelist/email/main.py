"""Primary runner for emailing finished price lists to customers"""

# standard imports
from dotenv import load_dotenv
import logging
import time
from pathlib import Path
import re

# third party imports
import pandas as pd

# internal imports
from config.paths import PRICE_LIST_ENV, PRICE_LIST_EMAILER_CFG
from utils.yaml_loader import load_yaml
from data_toolkit.attachment_mapper.acu_id import id_to_path_map
from data_toolkit.clients.salesforce import SFClient
from data_toolkit.cleaners.data_cleaner import DataCleaner
from pipelines.pricelist.email.bodies import external_email, internal_email, test_span_elements
from pipelines.pricelist.email.pricelist_email import BaseEmail, OutlookSender
from data_toolkit.clients.outlook import OLClient
from data_toolkit.clients.acumatica import AcumaticaClient

from collections import defaultdict

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format= "%(message)s")

PROD = False

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

    # cleaned_internal_contacts = DataCleaner(
    #     **cfg["salesforce"]["data"]["internal"]["clean_plan"]
    # ).clean(internal_contacts_df)

    # internal_contacts_cache = extract_contacts_from_df(cleaned_internal_contacts)

    customer_names = AcumaticaClient(
        **cfg["acumatica"]["auth"]
        ).odata(**cfg["acumatica"]["customers"], df=True)

    customer_names.columns = ["key", "value"]

    # Drop empty key rows (avoids {nan: nan})
    customer_names = customer_names.dropna(subset=["key"])
    customer_names = customer_names.set_index("key")["value"].to_dict()

    # used for placing customer name in internal emails
    cust_name_map = {k.strip(): v.strip().title() for k, v in customer_names.items()}

    # ============== Build Emails ========================

    with OLClient() as ol_app:
        pav_emails = [
            BaseEmail(
                recipients=recipients,
                subject=f"Peerless-AV Monthly Price List - {acct}",
                body=test_span_elements(),
                attachments=attachments
            )
            for acct, recipients in external_contacts_cache.items()
            if (attachments:= pav_attachments.get(acct, None))
        ]
        
        nep_emails = [
            BaseEmail(
                recipients=recipients,
                subject=f"Neptune Monthly Price List - {acct}",
                body=external_email("Neptune"),
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

        # ============ HOT LOOP! =======================

        emails = [*pav_emails, *nep_emails, *internal_pav_emails, *internal_nep_emails]

        breakpoint()

        for e in emails: #, *nep_emails, *internal_pav_emails, *internal_nep_emails]:
            OutlookSender(
                ol_app=ol_app,
                sent_on_behalf="sales@peerless-av.com",
                prod=PROD
            ).send(e)

        logger.info(f"\nPAV External Emails: {len(pav_emails)}")
        logger.info(f"\nNEP External Emails: {len(nep_emails)}")
        logger.info(f"\nPAV Internal Emails: {len(internal_pav_emails)}")
        logger.info(f"\nNEP Internal Emails: {len(internal_nep_emails)}")

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


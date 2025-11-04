"""Primary runner for emailing finished price lists to customers"""

# standard imports
from dotenv import load_dotenv
import logging
import time
from pathlib import Path

# third party imports
import pandas as pd

# internal imports
from config.paths import PRICE_LIST_ENV, PRICE_LIST_EMAILER_CFG
from utils.yaml_loader import load_yaml
from data_toolkit.attachment_mapper.acu_id import id_to_path_map
from data_toolkit.clients.salesforce import SFClient
from data_toolkit.cleaners.data_cleaner import DataCleaner
from pipelines.pricelist.email.bodies import correction_email
from pipelines.pricelist.email.pricelist_email import BaseEmail, OutlookSender
from data_toolkit.clients.outlook import OLClient
from utils.regex import extract_company_name

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format= "%(message)s")

PROD = True

def main():

    start_time = time.time()
    logger.info("Starting Emailer")

    load_dotenv(PRICE_LIST_ENV)

    cfg = load_yaml(PRICE_LIST_EMAILER_CFG)

    sf = SFClient(**cfg["salesforce"]["auth"], validate_at_init=True)

    # =========== External Resources ==============

    pav_attachments = id_to_path_map(Path(cfg["attachments"]["Peerless-AV"]))
    # nep_attachments = id_to_path_map(Path(cfg["attachments"]["Neptune"]))

    external_contacts_df = sf.query(
        cfg["salesforce"]["data"]["external"]["soql"]
    )

    cleaned_external_contacts = DataCleaner(
        **cfg["salesforce"]["data"]["external"]["clean_plan"]
    ).clean(external_contacts_df)

    external_contacts_cache = extract_contacts_from_df(cleaned_external_contacts)

    # ========= Internal Resources ============
    # internal_contacts_df = sf.query(
    #     cfg["salesforce"]["data"]["internal"]["soql"]
    # )

    # cleaned_internal_contacts = DataCleaner(
    #     **cfg["salesforce"]["data"]["internal"]["clean_plan"]
    # ).clean(internal_contacts_df)

    # internal_contacts_cache = extract_contacts_from_df(cleaned_internal_contacts)

    with OLClient() as ol_app:
        pav_emails = [
            BaseEmail(
                recipients=recipients,
                subject="Peerless-AV Monthly Price List - Correction",
                body=correction_email(),
                attachments=attachments
            )
            for acct, recipients in external_contacts_cache.items()
            if (attachments:= pav_attachments.get(acct, None))
        ]
        
        # nep_emails = [
        #     BaseEmail(
        #         recipients=recipients,
        #         subject="Neptune Monthly Price List",
        #         body=correction_email("Neptune"),
        #         attachments=attachments
        #     )
        #     for acct, recipients in external_contacts_cache.items()
        #     if (attachments:= nep_attachments.get(acct, None))
        # ]

        # internal_pav_emails = [
        #     BaseEmail(
        #         recipients=recipient,
        #         subject=f"Montly Price List - Not Distributed {...}",
        #         body="",
        #     )
        #     for acct, recipient in internal_contacts_cache.items()
        #     if pav_attachments.get(acct, None)
        # ]

        # internal_nep_emails = [
        #     BaseEmail(
        #         recipients=recipient,
        #         subject=f"Monthly Price List: {name}",
        #         body=""
        #     )
        #     for acct, recipient in internal_contacts_cache.items()
        #     if (name:= nep_attachments.get(acct, None))
        # ]

        for e in pav_emails:
            OutlookSender(
                ol_app=ol_app,
                sent_on_behalf="sales@peerless-av.com",
                prod=PROD
            ).send(e)

    
    end_time = time.time()

    # logger.info(
    #     f"\nLists not sent due to Price List Delivery To Salesperson \
    #     \nPAV: {internal_pav_email_count} \
    #     \nNeptune: {internal_nep_email_count} \
    #     \nTotal Not Sent: {internal_pav_email_count + internal_nep_email_count}"
    # )

    logger.info(f"Emailer Complete, elapsed time: {end_time - start_time}")






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


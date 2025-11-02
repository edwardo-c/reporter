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
from pipelines.pricelist.email.emailer import Emailer
from utils.yaml_loader import load_yaml
from data_toolkit.clients.salesforce import SFClient
from data_toolkit.cleaners.data_cleaner import DataCleaner
from data_toolkit.attachment_mapper.acu_id import id_to_path_map
from pipelines.pricelist.email.bodies import external_email, internal_email, external_nep_email

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format= "%(message)s")

PROD = True

def main():

    start_time = time.time()
    
    logger.info("Starting Emailer")

    load_dotenv(PRICE_LIST_ENV)

    cfg = load_yaml(PRICE_LIST_EMAILER_CFG)

    sf = SFClient(**cfg["salesforce"]["auth"], validate_at_init=True)

    pav_attachments = id_to_path_map(Path(cfg["attachments"]["Peerless-AV"]))
    nep_attachments = id_to_path_map(Path(cfg["attachments"]["Neptune"]))

    # =========== External Emails ==============

    external_contacts_df = sf.query(
        cfg["salesforce"]["data"]["external"]["soql"]
    )

    cleaned_external_contacts = DataCleaner(
        **cfg["salesforce"]["data"]["external"]["clean_plan"]
    ).clean(external_contacts_df)

    external_contacts_cache = extract_contacts_from_df(cleaned_external_contacts)

    with Emailer(
        contacts_cache=external_contacts_cache,
        attachments_cache=pav_attachments,
        email_body=external_email,
        prod=PROD,
        brand="Peerless-AV",
        add_attachments=True
    ) as pav:
        pav_email_count = pav.email()


    # email neptune lists
    with Emailer(
        contacts_cache=external_contacts_cache,
        attachments_cache=nep_attachments,
        email_body=external_nep_email,
        prod=PROD,
        brand="Neptune",
        add_attachments=True
    ) as nep:
        nep_email_count = nep.email()

    logger.info(
        f"\nExternal Lists sent:\
        \nPAV: {pav_email_count} out of {len(pav_attachments.keys())}\
        \nNEP: {nep_email_count} out of {len(nep_attachments.keys())}\
        \nTotal Sent: {pav_email_count + nep_email_count}"
    )

    # ============== Internal Emails ================

    # not ran yet due to unimplemented namiing extraction in the email

    # internal_contacts_df = sf.query(
    #     cfg["salesforce"]["data"]["internal"]["soql"]
    # )

    # cleaned_internal_contacts = DataCleaner(
    #     **cfg["salesforce"]["data"]["internal"]["clean_plan"]
    # ).clean(internal_contacts_df)

    # internal_contacts_cache = extract_contacts_from_df(cleaned_internal_contacts)   

    # # email PAV lists
    # with Emailer(
    #     contacts_cache=internal_contacts_cache,
    #     attachments_cache=pav_attachments,
    #     email_body=internal_email,
    #     prod=PROD,
    #     brand="Peerless-AV",
    #     add_attachments=False
    # ) as pav:
    #     internal_pav_email_count = pav.email()
    
    # # email neptune lists
    # with Emailer(
    #     contacts_cache=internal_contacts_cache,
    #     attachments_cache=nep_attachments,
    #     email_body=internal_email,
    #     prod=PROD,
    #     brand="Neptune",
    #     add_attachments=False
    # ) as nep:
    #     internal_nep_email_count = nep.email()
    
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


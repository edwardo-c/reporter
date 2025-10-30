"""Primary runner for emailing finished price lists to customers"""

# standard imports
from dotenv import load_dotenv
import logging
from os import getenv
import time

# third party imports
import pandas as pd

# internal imports
from config.paths import PRICE_LIST_ENV, PRICE_LIST_EMAILER_CFG
from pipelines.pricelist.email.emailer import PriceListEmailer
from utils.yaml_loader import load_yaml
from data_toolkit.clients.salesforce import SFClient
from data_toolkit.cleaners.data_cleaner import DataCleaner

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format= "%(asctime)s | %(message)s")


def _boilerplate_email(brand: str) -> str:
    return (
        f"<html><body>"
        f"<p><h3>Attached is your monthly <b>{brand}</b> price list.</h3></p>"
        f"<p>If you would like to be removed from, or add someone to, our distribution list, please reply to this email.</p>"
        f"<p>See the <b>Updates</b> tab for any changes from last month’s list.</p>"
        f"<p>- {brand} Sales Team</p>"
        f"</body></html>"
    )

def main():
    
    logger.info("Starting Emailer")

    load_dotenv(PRICE_LIST_ENV)

    cfg = load_yaml(PRICE_LIST_EMAILER_CFG)

    sf = SFClient(**cfg["salesforce"]["auth"], validate_at_init=True)

    internal_contacts_df = sf.query(cfg["salesforce"]["data"]["internal"]["soql"])

    cleaned_internal_contacts = DataCleaner(
        **cfg["salesforce"]["data"]["internal"]["clean_plan"]
    ).clean(internal_contacts_df)

    external_contacts_df = sf.query(cfg["salesforce"]["data"]["external"]["soql"])
    
    cleaned_external_contacts = DataCleaner(
        **cfg["salesforce"]["data"]["external"]["clean_plan"]
    ).clean(external_contacts_df)

    contacts_df = pd.concat([cleaned_internal_contacts, cleaned_external_contacts])

    breakpoint()

    with PriceListEmailer(
        contacts_df=contacts_df,
        files_dir=cfg["attachments"],
        email_body=_boilerplate_email,
        prod=False,
    ) as ple:
        email_count = ple.email()

    logger.info(f"sent {email_count} emails")
    
if __name__ == "__main__":
    main()

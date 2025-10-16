from pipelines.pricelist.email.emailer import send_emails
from dotenv import load_dotenv
from config.paths import PRICE_LIST_ENV, PRICE_LIST_EMAILER_CFG
from utils.yaml_loader import load_yaml
from os import getenv

from pipelines.pricelist.email.contacts import get_contacts


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
    
    print("Running Emailer")

    load_dotenv(PRICE_LIST_ENV)
    cfg = load_yaml(PRICE_LIST_EMAILER_CFG)

    email_count: int = send_emails(
        contacts=get_contacts(cfg["sf_auth"]),
        files_dir= {'Peerless-AV': getenv("PAV_ATTACHMENTS"), 
                    'Neptune': getenv("NEP_ATTACHMENTS")},
        email_body=_boilerplate_email
    )

    print(f"sent {email_count} emails")
    
if __name__ == "__main__":
    main()

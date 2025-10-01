from pipelines.pricelist.emailer import send_emails
from dotenv import load_dotenv
from config.paths import PRICE_LIST_ENV
from os import getenv

def _boilerplate_email():
    
    ...

def main():
    
    print("Running Emailer")

    load_dotenv(PRICE_LIST_ENV)
    
    contacts_file_path = getenv("CONTACTS")

    files_dir = {
        'pav': getenv("PAV_ATTACHMENTS"), 
        'nep': getenv("NEP_ATTACHMENTS")}
    
    email_body_map = {
        "pav": "pav body test",
        "nep": "nep body test"}


    send_emails(
        contacts_file_path=contacts_file_path,
        files_dir=files_dir,
        email_body_map=email_body_map
    )

if __name__ == "__main__":
    main()
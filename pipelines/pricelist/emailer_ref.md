# Price List Emailer

Specifically used for the Price List distribution of nep and pav brand

Goal: send a dynamic list of customers their specific file attachment.
Each file may be different, it is imperative that the customer get their specified file. Link between customer and file is account number which exists in the contacts csv and in the file name

How to use:

```
from pipelines.pricelist.emailer import send_emails
send_emails(...)
```

send_emails is a wrapper for the context manager of the PriceListEmailer class. Uses existing instance of Outlook or creates new instance.
Outlook is NOT exited at close so that emails continue to send

Args:

- contacts_file_path: csv path holding contacts. 
Required Columns: ["ACU Customer ID", "Email"]


**Crucial Detail!** 
***The BrandName listed in the following two arguements must exist in both. This is how the system knows which email body to use for each attachment***

- files_dir: {'BrandName': PathToDirHoldingFiles,}
Expected to be the finished price list files. 
6-9 Digit Acumatica ID must be present in the file name, that same ID is linked back to the ACU Customer ID column in the data from contacts_file_path

- email_body_map {'BrandName': 'html friendly email body',}
Used as the email body for each brand specific email


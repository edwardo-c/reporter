"""Email customer specific price list per brand"""

from pathlib import Path
from typing import Dict
import pandas as pd
import re
import time

from win32com.client import gencache, GetActiveObject
from utils.validators import valid_path

from typing import Callable

olMailItem = 0  # Outlook constant

def send_emails(
        contacts_file_path: Path,
        files_dir: dict,
        email_body: Callable):
    """
    Send emails with price list attachment to contacts
    using account number from file name as key

    args:
        - contacts_file_path: csv file path holding contacts; 
          Required Columns: ["ACU Customer ID", "Email"]
            
        - files_dir: {'BrandName': Path/To/Dir/Holding/Attachments,}
          File paths inside are expected to have 7-9 digit account number
-
        - email_body_map: callable function used for both brand emails,
          expects f{brand} in function for brand callout in body
    """
    with PriceListEmailer(
        contacts_file_path=contacts_file_path,
        files_dir=files_dir,
        email_body = email_body
    ) as e:
        return e.email()


class PriceListEmailer:
    def __init__(
            self, contacts_file_path: str, 
            files_dir: Dict[str, Path], 
            email_body: Callable):
        self._contacts_file_path = contacts_file_path
        self._files_dir = files_dir
        self._email_body = email_body

        self._outlook = None
        self._owns_outlook = False

    def __enter__(self):
        try:
            self._outlook = GetActiveObject("Outlook.Application")
        except Exception:
            self._outlook = gencache.EnsureDispatch("Outlook.Application")
            self._owns_outlook = True
        return self

    def __exit__(self, exc_type, exc, tb):
        # do not quit Outlook — let it finish sending
        self._outlook = None
        self._owns_outlook = False

    def email(self) -> int:
        """Main runner: matches contacts to files and sends mail."""
        contacts_cache = self._compile_contacts()
        files_cache = self._compile_file_cache()

        sent_count = 0
        for brand, file_map in files_cache.items():
            body = self._email_body(brand)
            for acct_num, file in file_map.items():
                contacts = contacts_cache.get(str(acct_num))
                if not contacts:
                    continue
                self._send_email(
                    contacts=contacts,
                    subject=f"{brand} Monthly Price List: {acct_num}",
                    body=body,
                    attachment=file,
                )
                sent_count += 1
        return sent_count

    def _send_email(
            self, *, 
            contacts: list[str], 
            subject: str, 
            body: str, 
            attachment: Path | None = None
        ):
        """Compose & send one message."""
        mail = self._outlook.CreateItem(olMailItem)
        mail.SentOnBehalfOfName = "sales@peerless-av.com"
        mail.To = "; ".join(c.strip() for c in contacts if c)
        mail.Subject = subject
        mail.HTMLBody = body
        if attachment:
            mail.Attachments.Add(str(attachment))

        mail.DeleteAfterSubmit = True  # don’t clog Sent Items
        # mail.Display()
        mail.Send()
        time.sleep(0.05)  # light throttle

    def _compile_contacts(self) -> dict[str, list[str]]:
        """Return {account -> [contacts]} from CSV."""
        contacts_path: Path = valid_path(self._contacts_file_path)
        if contacts_path.suffix != ".csv":
            raise NotImplementedError(f"unable to read {contacts_path.suffix} file")

        df = pd.read_csv(str(contacts_path))
        return (
            df.dropna(subset=["Email"])
              .query("Email != ''")
              .assign(
                  **{
                      "ACU Customer ID": df["ACU Customer ID"].astype(str).str.strip(),
                      "Email": df["Email"].astype(str).str.strip(),
                  }
              )
              .groupby("ACU Customer ID", sort=False)["Email"]
              .agg(list)
              .to_dict()
        )

    def _compile_file_cache(self) -> dict[str, dict[str, Path]]:
        """Return {'Brand': {acct: path} from files_dir"""
        def _extract_acct_num(s: Path | str) -> str | None:
            pattern = r"[A-Za-z0-9]{1,3}[0-9]{6}"
            m = re.search(pattern, str(s))
            return m[0] if m else None

        return {
            brand: {acct_num: f 
                    for f in Path(file_dir).glob("*.xlsx") 
                    if (acct_num := _extract_acct_num(f))} 
            for brand, file_dir in self._files_dir.items() 
        }
    
        

        # pav_glob = Path(self._files_dir["pav"]).glob("*.xlsx")
        # nep_glob = Path(self._files_dir["nep"]).glob("*.xlsx")

        # pav_map = {k: p for p in pav_glob if (k := _extract_acct_num(p))}
        # nep_map = {k: p for p in nep_glob if (k := _extract_acct_num(p))}

        # return {"pav": pav_map, "nep": nep_map}

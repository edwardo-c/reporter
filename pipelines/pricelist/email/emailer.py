"""Email customer specific price list per brand"""

from pathlib import Path
import time
from typing import Callable, Any
import re

from win32com.client import gencache, GetActiveObject

olMailItem = 0  # Outlook constant

"""
Send emails with price list attachment to contacts
using account number from file name as key

usage:
with PriceListEmailer(...) as ple:
    ...
"""

# ==================== DEPRECATED ========================

# class Emailer:
#     def __init__(
#             self, 
#             contacts_cache: dict[list[str]],
#             attachments_cache: dict[Path],
#             email_body: Callable,
#             brand: str,
#             prod: bool,
#             add_attachments: bool
#         ):
        
#         def _raise_if_empty(obj: Any, var_name: str):
#             if not obj:
#                 raise ValueError(f"{var_name} are empty!")
#             return obj

#         self.contacts_cache = _raise_if_empty(contacts_cache, "contacts")
#         self.attachments_cache = _raise_if_empty(attachments_cache, "attachments")
#         self.email_body = email_body
#         self.add_attachments = add_attachments
#         self.prod = prod
#         self.brand = brand
#         self._outlook = None
#         self._owns_outlook = False

#     def __enter__(self):
#         try:
#             self._outlook = GetActiveObject("Outlook.Application")
#         except Exception:
#             self._outlook = gencache.EnsureDispatch("Outlook.Application")
#             self._owns_outlook = True
#         return self

#     def __exit__(self, exc_type, exc, tb):
#         # do not quit Outlook — let it finish sending
#         self._outlook = None
#         self._owns_outlook = False
    
#     def email(self) -> int:
#         """Main runner: matches contacts to files and sends mail."""
#         sent_count = 0

#         body = self.email_body(self.brand)

#         for acct_num, contacts in self.contacts_cache.items():

#             attachment = self.attachments_cache.get(acct_num, None)
            
#             if not attachment:
#                 continue
#             else:
#                 if not self.add_attachments:
#                     body = self.email_body(extract_acct_name(Path(attachment).stem))
                
#                 self._send_email(
#                     contacts=contacts,
#                     subject=f"{self.brand} Monthly Price List: {acct_num}",
#                     attachment=attachment,
#                     body=body
#                 )

#                 sent_count += 1

#         return sent_count

#     def _send_email(
#             self, *, 
#             contacts: list[str], 
#             subject: str,
#             body: str,
#             attachment: str | None
#         ):
#         """Compose & send one message."""
#         mail = self._outlook.CreateItem(olMailItem)
#         mail.SentOnBehalfOfName = "sales@peerless-av.com"
#         mail.To = breakpoint()
#         mail.Subject = subject

#         if attachment and self.add_attachments:
#             mail.Attachments.Add(attachment)

#         mail.HTMLBody = body
#         mail.DeleteAfterSubmit = True

#         if self.prod:
#             mail.Send()
#         else:
#             mail.Display()
#             breakpoint()

#         time.sleep(0.05)  # light throttle


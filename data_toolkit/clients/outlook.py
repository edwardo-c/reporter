from win32com.client import gencache, GetActiveObject
from dataclasses import dataclass
from typing import Sequence


def get_outlook() -> object:
        """
        Connect to current outlook session or open new if no session exists
        """
        try:
            ol_app = GetActiveObject("Outlook.Application")
        except Exception:
            ol_app = gencache.EnsureDispatch("Outlook.Application")
        
        return ol_app

olMailItem = 0  # Outlook constant

@dataclass(slots=True)
class BaseEmail:
    to: str | Sequence[str]
    subject: str
    body: str | None
    sent_on_behalf_of: str | None
    delete_after_send: bool
    attachments: str | Sequence[str] | None = None

    def __post_init__(self) -> None:
        if isinstance(self.to, str):
            self.to = self.to
        else:
            self.to = "; ".join(r for r in self.to if r)

        if self.attachments is None:
            self.attachments = []
        elif isinstance(self.attachments, str):
            self.attachments = [self.attachments]
        else:
            self.attachments = self.attachments

class OutlookClient:
    def __init__(
            self, 
            ol_app: object | None,
            prod: bool = True
        ):

        self.ol_app = ol_app if ol_app else get_outlook()
        self.prod = prod

    def send_email(self, email: BaseEmail) -> None:

        if not isinstance(email, BaseEmail):
            raise TypeError(
                f"expected type BaseEmail, got {type(email.__name__)}"
                f"see data_toolkit.clients.outlook_sender.BaseEmail"
            )


        mail = self.ol_app.CreateItem(olMailItem)

        if email.sent_on_behalf_of:
            mail.SentOnBehalfOfName = email.sent_on_behalf_of

        if email.delete_after_send:
            mail.DeleteAfterSubmit = email.delete_after_send

        mail.To = email.to
        mail.Subject = email.subject
        mail.HTMLBody = email.body or ""
        
        for path in email.attachments:
            mail.Attachments.Add(path)

        if self.prod:
            mail.Send()
        else:
            mail.Display()  # preview
            breakpoint()
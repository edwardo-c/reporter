from dataclasses import dataclass, field
from typing import Sequence, Mapping, Any

olMailItem = 0  # Outlook constant

@dataclass(slots=True)
class BaseEmail:
    recipients: str | Sequence[str]
    subject: str
    body: str | None
    attachments: str | Sequence[str] | None = None

    # normalized
    to: str = field(init=False)
    _attachments: list[str] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if isinstance(self.recipients, str):
            self.to = self.recipients.strip()
        else:
            self.to = "; ".join(r.strip() for r in self.recipients if r)

        if self.attachments is None:
            self._attachments = []
        elif isinstance(self.attachments, str):
            self._attachments = [self.attachments]
        else:
            self._attachments = [a for a in self.attachments if a]

class OutlookSender:
    def __init__(self, ol_app: object, *, sent_on_behalf: str | None = None, prod: bool = False):
        self._ol_app = ol_app
        self._sent_on_behalf = sent_on_behalf
        self._prod = prod

    def send(
        self,
        email: BaseEmail | None = None,
        *,
        recipients: str | Sequence[str] | None = None,
        subject: str | None = None,
        body: str | None = None,
        attachments: str | Sequence[str] | None = None,
        delete_after_submit: bool = True,
    ) -> None:
        """
        One-size-fits-many API:
        - Pass a BaseEmail OR loose args (recipients/subject/body/attachments).
        """
        if email is None:
            email = BaseEmail(
                recipients=recipients or "",
                subject=subject or "",
                body=body,
                attachments=attachments,
            )

        mail = self._ol_app.CreateItem(olMailItem)
        if self._sent_on_behalf:
            mail.SentOnBehalfOfName = self._sent_on_behalf

        mail.To = email.to
        mail.Subject = email.subject
        mail.HTMLBody = email.body or ""
        mail.DeleteAfterSubmit = delete_after_submit

        for path in email._attachments:
            mail.Attachments.Add(path)

        if self._prod:
            mail.Send()
        else:
            mail.Display()  # preview in dev
            breakpoint()


def send_emails(emails_to_send: list[BaseEmail], prod: bool) -> int:
    """
    convenience wrapper -
    allows user pass in pre-built BaseEmails for sending
    if prod = true, emails will be sent, else breakpoint() to inspect first email

    CAUTION: 
    performance degraded if using more than once due to 
    bind (and re-bind) of outlook instance (see OLClient)
    if using multiple [BaseEmails], use seperate adapter for performance boost
    """
    sent_count = 0
    from data_toolkit.clients.outlook.outlook import OLClient

    with OLClient() as ol_app:
        sender = OutlookSender(
            ol_app,
            sent_on_behalf="sales@peerless-av.com",
            prod=prod
        )
        
        for e in emails_to_send:
            sender.send(e)
            sent_count += 1
    
    return sent_count
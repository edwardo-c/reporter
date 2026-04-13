# construction of base email resources

from data_toolkit.clients.outlook import BaseEmail
from pathlib import Path

"""
I need to be able to add a static attachment per brand
also need to be able to use seperate email bodies per brand
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class PriceListEmailBase:
    subject: str
    body: str
    sent_on_behalf_of: str
    delete_after_send: bool

def assemble_base_emails(
        attachment_map: dict[str, Path],
        contact_map: dict[str, list[str]],
        base_settings: PriceListEmailBase | dict[str, str | bool],
        static_attachments: Path | list[Path] | None = None
    ) -> list[BaseEmail]:
    """
    Creates a BaseEmail for each attachment in attachment_map who
    has contacts in contact_map

    base_settings: general settings applied to all BaseEmails
    
    static_attachment: attachment(s) to be applied to all BaseEmails
    """

    if isinstance(base_settings, dict):
        base_settings = PriceListEmailBase(**base_settings)
    elif not isinstance(base_settings, PriceListEmailBase):
        raise TypeError(
            f"invalid base_settings input\n" 
            f"expected dict or PriceListEmailBase object"
        )

    result = []

    if isinstance(static_attachments, Path):
        static_attachments = [static_attachments]
    else:
        static_attachments = []

    for acu_id, attchment in attachment_map.items():
        
        contacts = contact_map.get(acu_id, None)

        if contacts:
            result.append(
                BaseEmail(
                    to=contacts,
                    subject=base_settings.subject,
                    body=base_settings.body,
                    sent_on_behalf_of=base_settings.sent_on_behalf_of,
                    delete_after_send=base_settings.delete_after_send,
                    attachments=[str(a) for a in [attchment, *static_attachments]]
                )
            )
        
    return result
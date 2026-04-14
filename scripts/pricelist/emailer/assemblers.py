# construction of base email resources

from data_toolkit.clients.outlook import BaseEmail
from pathlib import Path
from dataclasses import dataclass
from scripts.pricelist.emailer.mappers import Mappers
from scripts.pricelist.emailer.settings import AppSettings
from scripts.pricelist.emailer.settings import BatchSettings

import pandas as pd
import re
from datetime import date

DATE_PART = r"\b[0-9]{2}\.[0-9]{2}\b"
YEAR = r"\b20[0-9]{2}\b"

@dataclass(frozen=True, slots=True)
class OutputResources:
    emails: list[BaseEmail]
    results_log: pd.DataFrame

def resolve_multiple_attachments(attachments: list[Path]) -> Path:
    """
    checks if multiple attachments exist, resolved if so
    otherwise pass through
    """

    date_map = {}

    if len(attachments) > 1:
        
        largest = None

        for a in attachments:
            
            date_part = re.match(DATE_PART, a.stem)
            
            year = re.match(YEAR, a.stem)
            
            if date_part and year:
                m, d = str(date_part.group[0]).split(".")
                d = date(year, m, d)
            
                if largest is None:
                    largest = d
                else:
                    largest = max(largest, d)
            
                date_map[d] = a

    if date_map == {}:
        return attachments[0]
    else:
        return date_map[largest]

def build_base_email(
        contacts: list[str],
        attachments: list[Path],
        batch_settings: BatchSettings
    ) -> BaseEmail:
    
    attachment = resolve_multiple_attachments(attachments)
    
    if batch_settings.static_attachments:
        attachments = [attachment, *batch_settings.static_attachments]

    return BaseEmail(
        to=contacts,
        subject=batch_settings.email_settings.subject,
        body=batch_settings.email_settings.body,
        sent_on_behalf_of=batch_settings.email_settings.sent_on_behalf_of,
        delete_after_send=batch_settings.email_settings.delete_after_send,
        attachments=attachments
    )

def assemble_outputs(
        mappers: Mappers,
        app_settings: AppSettings,
        results_log: dict[str, list[str]]
    ) -> OutputResources:
    """
    builds BaseEmail objects to be sent and results log of what was found

    resolves multiple attachments and adds in static attachments

    """
    emails = []

    all_accounts = (
        sorted(
            set(mappers.pav_map.attachment_map.keys())
            .union(mappers.nep_map.attachment_map.keys())
        )
    )

    for acct in all_accounts:

        results_log["acu_id"].append(str(acct))
        
        contacts = mappers.contact_map.get(acct, None)
        results_log["contacts"].append(str(contacts))

        if acct in mappers.pav_map.attachment_map:
            results_log["pav_created"].append(str(True))
            if contacts:
                emails.append(
                    build_base_email(
                        contacts=contacts,
                        attachments=mappers.pav_map.get_attachment(acct),
                        batch_settings=app_settings.PAVSettings
                    )
                )
        else:
            results_log["pav_created"].append(str(False))


        if acct in mappers.nep_map.attachment_map:
            results_log["nep_created"].append(str(True))
            if contacts:
                emails.append(
                    build_base_email(
                        contacts=contacts,
                        attachments=mappers.nep_map.get_attachment(acct),
                        batch_settings=app_settings.NEPSettings
                    )
                )
        else:
            results_log["nep_created"].append(str(False))
        
    return OutputResources(
        emails=emails,
        results_log=results_log
    )
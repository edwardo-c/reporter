from enum import Enum

class RecipientLogSchema(Enum):
    ACCT = "Acumatica Account Number"
    PAV = "Peerless-AV List Created"
    NEP = "Neptune List Created"
    EXT = "External Price List Recipient(s)"
    INT = "Internal Price List Recipient(s)"
    SENT_TO = "Price List Sent To"

class RecipientLogSentToVals(Enum):
    EXT = "external only"
    INT = "internal only"
    NA = "not sent, no contacts found"

class RecipientLogNone(Enum):
    NA = "none"
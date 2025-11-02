"""Common internal regex patterns and helpers"""

import re

def extract_company_name(s: str | None) -> str | None:
    """
    Returns the string after the " - " typically found in standard naming convention
    AcctID - AcctName
    """
    if not s:
        return None
    
    acct_name_pattern = r"[A-Za-z0-9]{1,3}[0-9]{6}\s-\s(.*)"
    
    acct_name = re.search(acct_name_pattern, s)
    
    if acct_name:
        return acct_name.group(1)
        
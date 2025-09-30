"""Email customer specific price list per brand"""

from pathlib import Path
import pandas as pd
import re

from utils.validators import valid_path

def _boilerplate_emails():
    nep = """
    ...
    """
    pav = """
    ...
    """

    return {'nep': nep, 'pav': pav}

class PriceListEmailer():
    """
    Send emails to contacts using account number as key
    
    args:
        _contacts_file_path: csv file path holding contacts
            expected account number and contact per row
        _files_dir: dict['pav':Path, 'nep': Path]. Path equals the 
            files to be attached to the email
        _email_body_map: dict['pav': str, 'nep': str]
            map containing email body for each brand
    """
    def __init__(self, 
            contacts_file_path: str,
            files_dir: dict[str, Path],
            email_body_map: dict[str, str]):
        self._contacts_file_path = contacts_file_path
        self._files_dir = files_dir
        self._email_body_map = email_body_map
        # self.results = None TODO: define contract for output

    def __enter__(self):
        return self

    def __exit__():
        ...

    """TODO: set up guardrails for matching email body
    map to matching files dir""" 

    def email(self):
        """primary runner for PriceListEmailer"""

        contacts_cache = self._compile_contacts()
        files_cache = self._compile_file_cache()

        # loop through files checking for contacts
        for brandKey, file_cache in files_cache.items():
            body = self._email_body_map[brandKey]
            for acct_num, file in file_cache.items():
                contacts = contacts_cache.get(acct_num)
                if contacts:
                    breakpoint()
                    self._send_email(
                        attachment=file, 
                        body=body, 
                        contacts=contacts)

    def _send_email(
            self, 
            attachment: Path,
            body: str, contacts: list
            ):
        breakpoint()

    def _compile_contacts(self) -> dict[str, Path]:
        """
        generate account number: contacts dictionary from path
        Expected in _contacts_file_path data:
            one row per account number, single contact per row
            csv file
        """
        
        def _sfx_check(sfx: str, expected: str):
            if not sfx == expected:
                raise NotImplementedError(f"unable to read {sfx} file")
        
        contacts_path: Path = valid_path(self._contacts_file_path)
        _sfx_check(contacts_path.suffix, ".csv")

        df = pd.read_csv(str(contacts_path))

        out = (df.dropna(subset=["Email"])           # drop NaN contacts
         .query("Email != ''")                       # drop empty strings
         .groupby("ACU Customer ID", sort=False)     # group by account
         ["Email"]                                   # look at contacts
         .agg(list)                                  # collect into lists
         .to_dict())                                 # spit out {acct: [contacts]}

        return out
    
    def _compile_file_cache(self):
                
        pav_glob = list(Path(self._files_dir["pav"]).glob("*.xlsx"))
        nep_glob = list(Path(self._files_dir["nep"]).glob("*.xlsx"))

        def _extract_acct_num(s: str):
            pattern = r"[a-zA-Z0-9]{1,3}[0-9]{6}"
            match = re.search(pattern=pattern, string=str(s))
            if match:
                return match[0]
            else:
                return None

        pav_map = {_extract_acct_num(p):p for p in pav_glob}
        nep_map = {_extract_acct_num(p):p for p in nep_glob}

        return {'pav': pav_map, 'nep': nep_map}
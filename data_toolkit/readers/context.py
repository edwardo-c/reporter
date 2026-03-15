from simple_salesforce import Salesforce

class ReaderContext:
    def __init__(self, sf: Salesforce | None = None):
        self.sf = sf
        
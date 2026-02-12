"""
get a report from sf
get the grouped totals
send an email to each
"""

from data_toolkit.salesforce.client import SFClient
from utils.yaml_loader import load_yaml
from dotenv import load_dotenv



"""
expected to hold the email address
"""

def main():
    
    load_dotenv()

    cfg = load_yaml()

    sf = SFClient()


if __name__ == "__main__":
    ...
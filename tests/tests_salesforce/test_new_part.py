from dotenv import load_dotenv
import os

import pytest

from config.paths import SF_CRED
from salesforce.client import SFClient
from salesforce.ids import registry
from salesforce.objects.new_part import NewPart
from salesforce.objects.msrp_entry import MSRPEntry

@pytest.fixture(scope="session", autouse=True)
def load_env():
    loaded = load_dotenv(SF_CRED, override=True)
    assert loaded, f"Failed to load dotenv file at {SF_CRED}"

def test_env_path_exists():
    assert SF_CRED.exists()

@pytest.fixture
def client():
    with SFClient(
        username=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD"),
        security_token=os.getenv("SECURITY_TOKEN")
    ) as client:
        yield client

@pytest.fixture
def new_part_id(client):
    
    np = NewPart(
        name="UniqueTestPart_01",
        category="MOUNT",
        acu_status="Active",
        acu_pmplcm="Active",
        acu_auth_required=True,
        description="Hello from Python!",
        price_group="CORE"
    )

    new_part = client.insert_record("Product2", np.params)
    
    soql = """
        SELECT 
            Id,
            Name
        FROM Product2 
        WHERE Name = 'UniqueTestPart_01'
    """

    result = client.query(soql=soql, df=False)
    
    id = result[0]["Id"]
    assert id == new_part["id"]

    yield id

    try:
        client.delete_record("Product2", id)
    except Exception as e:
        print(f"Cleanup failed: {e}")

def test_price_grp_id():
    assert registry.price_grp_id("TEST") == "pytest"
    assert registry.price_grp_id("missing") == None

def test_msrp_id():
    assert registry.MSRP_ID == "01s6A000001t7RtQAI"

def test_price_entries(client, new_part_id):

    price = 999.99
    msrp = MSRPEntry(price=price, id=new_part_id)
    client.insert_record("PricebookEntry", msrp.params)

    soql = f"""
        SELECT 
            Id,
            Name,
            (SELECT Id, Pricebook2Id, UnitPrice FROM PricebookEntries),
            (SELECT Id, Price_List_Price__c FROM Price_List_Entries__r)
        FROM Product2
        WHERE Id = '{new_part_id}'
    """

    breakpoint()

    result = client.query(soql=soql, df=False)
    msrp_result = float(result[0]["PricebookEntries"]["records"][0]["UnitPrice"])
    
    # assert price == float(result[0]["UnitPrice"])

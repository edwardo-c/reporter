import pytest
from salesforce.ids import registry
from salesforce.client import SFClient
from dotenv import load_dotenv
from config.paths import SF_CRED
import os
from salesforce.objects.new_part import NewPart

@pytest.fixture(scope="session", autouse=True)
def load_env():
    loaded = load_dotenv(SF_CRED, override=True)
    assert loaded, f"Failed to load dotenv file at {SF_CRED}"

def test_env_path_exists():
    assert SF_CRED.exists()

def test_price_grp_id():
    assert registry.price_grp_id("TEST") == "pytest"
    assert registry.price_grp_id("missing") == None

def test_msrp_id():
    assert registry.MSRP_ID == "01s6A000001t7RtQAI"

def test_new_part():

    np = NewPart(
        name="UniqueTestPart_01",
        category="MOUNT",
        acu_status="Active",
        acu_pmplcm="Active",
        acu_auth_required=True,
        description="Hello from Python!",
        price_group="CORE"
    )

    with SFClient(
        username=os.getenv("USERNAME"),
        password=os.getenv("PASSWORD"),
        security_token=os.getenv("SECURITY_TOKEN")
    ) as client:
        client.upload_part(
            part_params=np.params, 
            msrp=999.99
        )
    

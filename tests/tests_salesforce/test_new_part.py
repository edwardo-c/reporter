from salesforce.ids import registry

def test_price_grp_id():
    assert registry.price_grp_id("TEST") == "pytest"
    assert registry.price_grp_id("missing") == None
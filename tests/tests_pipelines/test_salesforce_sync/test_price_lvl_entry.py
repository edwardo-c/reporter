import pytest
from salesforce.objects.price_lvl_entry import bulk_arrange_price_lvls

def test_create_entries():
    
    parts_to_organize = {'ABC', 'DEF'}
    parts_data_dict = {
        'ABC': {
            'Category': None,
            'Dealer': '1875.000000',
            'Distributor': '1695.000000',
            'Partner': '1790.000000',
            'PriceGroup': 'DVLED',
            'Special': '1615.000000',
            'sf_id': '123456'
            },
        'DEF': {
            'Category': None,
            'Dealer': '100',
            'Distributor': '200',
            'Partner': '300',
            'PriceGroup': 'CORE',
            'Special': '400',
            'sf_id': '999000'},
        }
    
    entries = bulk_arrange_price_lvls(parts_to_organize=parts_to_organize, data_dict=parts_data_dict)
    for e in entries:
        breakpoint()
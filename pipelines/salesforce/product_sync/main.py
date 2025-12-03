"""scaffolding for product sync procedure from Acumatica to Salesforce"""

from data_toolkit.clients.acumatica import AcumaticaClient
from data_toolkit.clients.salesforce import SFClient
from utils.yaml_loader import load_yaml
from dotenv import load_dotenv
from config.paths import SALESFORCE_PRODUCT_SYNC_CFG, SALESFORCE_PRODUCT_SYNC_ENV

from salesforce.objects.new_part import NewPart, bulk_arrange
from salesforce.objects.msrp_entry import bulk_arrange_msrp
from salesforce.objects.price_lvl_entry import bulk_arrange_price_lvls

def main():
    
    load_dotenv(SALESFORCE_PRODUCT_SYNC_ENV)
    cfg = load_yaml(SALESFORCE_PRODUCT_SYNC_CFG)

    # ========== Source of Truth ==========
    acu_cfg = cfg["acumatica"]
    
    acu_client = AcumaticaClient(**acu_cfg["auth"])

    acu_raw = acu_client.odata(**acu_cfg["odata"], df=False)

    acu_data_dict = {
        r["PartNumber"].strip():
        {k: v for k, v in r.items() if k != 'PartNumber'}
        for r in acu_raw
    }

    # ========== Should match Truth ==========
    sf_cfg = cfg["salesforce"]

    sf_client = SFClient(**sf_cfg["auth"])

    sf_raw = sf_client.query(sf_cfg["soql_query"], df=False)

    sf_data = set(r["Name"].strip() for r in sf_raw)

    # ========= Identify missing ===========
    truth = set(acu_data_dict.keys())
    
    missing = truth.difference(sf_data)

    if not missing:
        # TODO: logging message
        SystemExit()
    else:
        missing_parts_data_dict = {
            m: 
            acu_data_dict[m]
            for m in missing
    }

    new_parts: list[NewPart] = bulk_arrange(missing, missing_parts_data_dict)

    # ======== HOT LOOP: Upload Records ============

    for np in new_parts:
        if np.valid:
            resp = sf_client.insert_record("Product2", data=np.params)
            if resp["success"]:
                sf_id = resp["id"]
                missing_parts_data_dict[np.name]["sf_id"] = sf_id

    msrp_entries = bulk_arrange_msrp(missing, missing_parts_data_dict)
    
    for msrp_entry in msrp_entries:
        if msrp_entry.valid:
            sf_client.insert_record("PricebookEntry", data=msrp_entry.params)

    price_lvl_entries = bulk_arrange_price_lvls(missing, missing_parts_data_dict)
    for lvl_entry in price_lvl_entries:
        if lvl_entry.valid:
            sf_client.insert_record("Price_List_Entry__c", data=lvl_entry.params)

if __name__ == '__main__':
    main()


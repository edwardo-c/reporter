"""Arrangement of Acumatica -> Salesforce product sync data"""
import pandas as pd
import duckdb
from simple_salesforce import Salesforce

def upload_new_parts(
        sf: Salesforce, 
        acumatica_df: pd.DataFrame, 
        salesforce_df: pd.DataFrame,
        price_list_key_to_id: dict[str, str],
        standard_price_book_id: str,
        price_group_key_to_id):
    "arrange upload dict per missing part"

    # normalize join column
    salesforce_df = _standardize_join_col(df=salesforce_df, col_name="Name")
    acumatica_df = _standardize_join_col(df=acumatica_df, col_name="PartNumber")

    float_cols = ["Dealer", "Partner", "Distributor","Special", "MSRP"]

    parts_to_upload = (
        acumatica_df
        .merge(salesforce_df, how="left", on="_join_col", indicator=True)
        .query('_merge == "left_only"')
        .drop(columns=["_merge", "_join_col", "Name"])
        # Cast non-float columns to string
        .pipe(lambda d: d.astype({c: "string" for c in d.columns if c not in float_cols}))
        # Strip whitespace for all string columns
        .pipe(lambda d: d.apply(lambda col: col.str.strip() if col.dtype == "string" else col))
        # Convert float-like columns to numeric
        .pipe(lambda d: d.assign(**{
            c: lambda x, c=c: pd.to_numeric(x[c], errors="coerce").round(2)
            for c in float_cols if c in d.columns}))
        .assign(PriceGroupId=lambda d: d["PriceGroup"].map(price_group_key_to_id))
    )

    pricing_to_upload: pd.DataFrame = (
        parts_to_upload
        # convert to long data for single upload per row
        .melt(
            id_vars=["PartNumber", "PriceGroup", "Description"],
            value_vars=float_cols,
            var_name="PriceLevel",
            value_name="Price",)
        # id mapping
        .assign(PriceListKey=lambda d: d["PriceGroup"].str.upper() + "|" + d["PriceLevel"].str.upper())
        .assign(PriceListId=lambda d: d["PriceListKey"].map(price_list_key_to_id)
    ))

    new_part_ids: dict[str, str] = _upload_new_parts(sf, parts_to_upload)

    msrp_upload = pricing_to_upload[pricing_to_upload["PriceLevel"] == "MSRP"]
    price_list_entries = pricing_to_upload[pricing_to_upload["PriceLevel"] != "MSRP"]

    _upload_msrp_pricing(sf, msrp_upload, standard_price_book_id, new_part_ids)
    _upload_price_list_entries(sf, price_list_entries, new_part_ids)

def _upload_new_parts(sf: Salesforce, parts_to_upload: pd.DataFrame) -> dict[str, str]:
    """uploads new parts to salesforce, returns partnumber: id"""
    out = {}
    for r in parts_to_upload.itertuples():
        
        result = sf.Product2.create({
            "Name": r.PartNumber,
            "CurrencyIsoCode": "USD",
            "Price_Group__c": r.PriceGroupId,
            "IsActive": True, 
            "SBQQ__QuantityEditable__c": True,
            "Part_Number__c": r.PartNumber,
            "ProductCode": r.PartNumber,
            "Description": r.Description})
        
        if result["success"]:
            out[r.PartNumber] = result['id']
        
        # left in for testing
        break

    return out

def _upload_msrp_pricing(
        sf: Salesforce, 
        upload_df: pd.DataFrame, 
        standard_price_book_id: str,
        part_to_id_map: dict[str, str]
    ):

    for r in upload_df.itertuples():
        id = part_to_id_map.get(r.PartNumber, None)
        if id:
            sf.PricebookEntry.create({
                "Product2Id": id, 
                "Pricebook2Id": standard_price_book_id, 
                "UnitPrice": r.Price,
                "IsActive": True,
                "CurrencyIsoCode": "USD"})

def _upload_price_list_entries(
        sf: Salesforce, 
        upload_df: pd.DataFrame,
        new_part_ids: dict
    ):
    for r in upload_df.itertuples():
        id = new_part_ids.get(r.PartNumber, None)
        if id:
            breakpoint()
            sf.Price_List_Entry__c.create({
                "Active__c": True,
                "CurrencyIsoCode": "USD",
                "Price_List__c": r.PriceListId,
                "Price_List_Price__c": r.Price,
                "Product__c": id
            })

def _standardize_join_col(df: pd.DataFrame, col_name: str):
    """Used for cleaning join column"""
    copy = df.copy()
    copy["_join_col"] = copy[col_name].str.casefold().str.strip()
    return copy
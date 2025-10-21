"""Arrangement of Acumatica -> Salesforce product sync data"""
import pandas as pd
import duckdb
from simple_salesforce import Salesforce

def upload_new_parts(
        sf: Salesforce, 
        acumatica_df: pd.DataFrame, 
        salesforce_df: pd.DataFrame,
        id_map: dict[dict[str, str]]):
    "arrange upload dict per missing part"

    # identify missing parts
    missing_parts: pd.DataFrame = (
        (_standardize_col(acumatica_df, "PartNumber"))
        .merge(_standardize_col(salesforce_df, "Name"), 
               how="left", left_on='PartNumber', right_on='Name', indicator=True)
        .query('_merge == "left_only"')
        .drop(columns=["Name", "_merge"])
    ).melt(
        id_vars=["PartNumber", "PriceGroup", "Description"],
        value_vars=["Dealer", "Partner", "Distributor","Special", "MSRP"],
        var_name="PriceLevel",
        value_name="Price")

    breakpoint()

    float_cols = [
        "Dealer", "Partner", "Distributor", 
        "Special", "MSRP"]
    upper_cols = ["PartNumber", "PriceGroup"]
    str_cols = ["Description"]

    cleaned = (
        missing_parts
        # 1) force numeric (coerce bad values to NaN), then round(2)
        .assign(**{
            c: (lambda d, c=c: pd.to_numeric(d[c], errors="coerce").round(2))
            for c in float_cols})
        # 2) clean strings: strip + upper (use pandas "string" dtype)
        .assign(**{
            c: (lambda d, c=c: d[c].astype("string").str.strip().str.upper())
            for c in upper_cols})
        # 3) clean strings: strip, retain case 
        .assign(**{
            c: (lambda d, c=c: d[c].astype("string").str.strip())
            for c in str_cols}))

    price_group_map = id_map["price_group"]
    standard_price_book = id_map["standard_price_book"]


    for r in cleaned.to_dict("records"):
        
        part_number = r.get("PartNumber", None)

        if part_number:
            
            breakpoint()

            # create new part
            result = sf.Product2.create({
                "Name": part_number,
                "CurrencyIsoCode": "USD",
                "Price_Group__c": price_group_map.get(r["PriceGroup"]),
                "IsActive": True, 
                "SBQQ__QuantityEditable__c": True,
                "Part_Number__c": part_number,
                "ProductCode": part_number,
                "Description": r["Description"]})  
            
            # add prices 
            if result["success"]:
                
                id = result["id"]
                
                # list/msrp price
                sf.PricebookEntry.create({
                    "Product2Id": id, 
                    "Pricebook2Id": standard_price_book, 
                    "UnitPrice": r["MSRP"],
                    "IsActive": True,
                    "CurrencyIsoCode": "USD"})
            
                # price list prices
                price_list__c = ""

                # sf.Price_List_Entry__c.create()
                

        

def _standardize_col(df: pd.DataFrame, col_name: str):
    copy = df.copy()
    copy[col_name] = copy[col_name].str.casefold().str.strip()
    return copy
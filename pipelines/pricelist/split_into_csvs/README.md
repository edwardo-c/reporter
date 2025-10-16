# Split Into CSVs

## What It Does
- Returns data via OData Feed
- Groups data by account number and brand
- Exports each group into seperate CSV file into destination folder

## Why It Matters
Created as a supplement to a VBA app that takes customer specific 
pricing (csv) files and generates a "Price List" for each. 
The odata feed contains our entire pricing catalog of all customers
The VBA app creates a price file by customer AND brand. 
We needed a way to split the data for each customer/brand for
injestion of the VBA app.

## How To Run
- Update config.pricelist.env 
    - update Effective Date on server side as needed
    - 'NEP_OUT': directory where NEP brand files land
    - 'PAV_OUT': directory where PAV brand files land 
    - activate virtual environment
    - python -m pipelines.pricelist.split_into_csvs.main
# Price List Automation

## What It Does
- Appends files inside a directory into a single data frame
- Groups dataframe by account numbers and brand
- Exports each group into seperate CSV file into destination folder

## Why It Matters
Created as a supplement to a VBA app that takes customer specific 
pricing (csv) files and generates a "Price List" for each. 
The (5) files inside the directory is the entire pricing catalog
for our ~700 customers. The VBA app creates a price file by customer
AND brand. We needed a way to split the data for each group for
injestion of the VBA app.

## How To Run
- Update config.pricelist.env 
    - 'SRC' to directory containing price catalog files
    - 'NEP_OUT' to directory where NEP brand files land
    - 'PAV_OUT' to directory where PAV brand files land 
    - activate virtual environment
    - python -m pipelines.pricelist.main

-------------------------------------

- create via VBA script

- manually create any left overs with unimplemented pipeline
    - Powerhouse
    - Visions
    - Grainger  

- copy ENs with seperate naming via python -m pipelines.pricelist.run_renamer

- Manual upload to peernet
- Manual salesforce notification to sales reps
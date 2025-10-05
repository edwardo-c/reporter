# Price List Emailer

## What It Does
Emails customers their specific Price List (attachment) for
two brands. Uses active outlook client for individual sending

## Why It Matters
Enables us to react to price changes faster by automating and distribution of customer specific price lists. 

## How To Use
- Update config.pricelist.env
    - NEP_ATTACHMENTS: dir holding finished NEP price list files 
    - PAV_ATTACHMENTS: dir holding finished PAV price list files
    - CONTACTS: latest export of contacts
    - python -m pipelines.pricelist.email_finished_lists.main


# Price List Automation

Created as a supplement to the VBA price list application
- export all price classes from Acumatica after 3pm
- place into price class folder on sales ops drive
- **Update config.pricelist.env** as needed
    - SRC = directory holding all price class exports
    - NEP_OUT: directory where seperated nep files will  land (csv)
    - PAV_OUT: directory where seperated pav files will land (csv)
- split into csvs with python -m pipelines.pricelist.main
- create via VBA script

- manually create any left overs with unimplemented pipeline
    - Powerhouse
    - Visions
    - Grainger  

- copy ENs with seperate naming via python -m pipelines.pricelist.run_renamer

- Manual upload to peernet
- Manual salesforce notification to sales reps
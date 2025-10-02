# Price List Automation

Created as a supplement to the VBA price list application
- export all price classes from Acumatica after 3pm
- place into price class folder on sales ops drive
- **Update config.pricelist.env** as needed
- split into csvs with python -m pipelines.pricelist.main
- create via VBA script

- manually create any left overs with unimplemented pipeline
    - Powerhouse
    - Visions
    - Grainger  

- copy ENs with seperate naming via python -m pipelines.pricelist.run_renamer

- Manual upload to peernet
- Manual salesforce notification to sales reps
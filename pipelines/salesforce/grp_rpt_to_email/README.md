# Group Report To Email

Configurable pipeline that emails single-grouped (OWNER_EMAIL) Salesforce reports using
a user-specified aggregate.

## Why This Exists

Sales Ops often has predefined tabular reports in Salesforce that require sales reps' attention. 
This pipeline emails the sales rep a specified aggregated value from the report.
Intended to be used when a Salesforce report can be grouped by the intended email recipient.

Salesforce -> Outlook -> Send email to sales rep

## Features
- Simple Salesforce query of report by ID
- Guards against improperly formatted report
- Compiling and sending of all emails
- PROD flag for inspecting an email or running the pipeline

## Structure

├─ pipelines/
    └─ salesforce/
        └─ grp_rpt_to_email/
        └─ main.py            # primary runner
        └─ cfgs/              # configurations used as inputs to the pipeline
        └─ email_bodies/
            └─ bodies.py      # html wrapped email bodies
            └─ registry.py    # convenience registry for returning email bodies
        

## Quick Start Guide

venv/scripts/activate
update CFG_FILE_NAME to name of config to be used
python -m pipelines.salesforce.grp_rpt_to_email.main

## Configuration

```
credentials:
  username: ${SF_USERNAME}          # must exist in env vars
  password: ${SF_PASSWORD}          # must exist in env vars
  security_token: ${SF_TOKEN}       # must exist in env vars

report:
  id: "OO0...."                     # can be found in report's url 
  agg_key: "RowCount"               # configurable, metric to be used in the email body
  
email:
  subject: "Overdue Opportunities Notification"
  body_func_key: "function_id"      # string identifier, mapped in registry
```
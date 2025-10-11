# status_report.main

## What It Does
Creates a 'status report' for customers with a program funding agreement.
Refreshes data in the sales table.
    __Sales table includes one row per part purchased__
    _Does NOT include sales rep credit - multiple reps get credit for one row so_
    _that would be inacurate of the customers' sales._

## Why it Exists
Needed a simple way to generate multiple reports. These reports inform a
customer of how much they have to spend in order to receive rebates.
Now we can notify them monthly of their progress.

## How To Run
python -m pipelines.status_reports.main
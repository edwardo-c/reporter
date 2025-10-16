[RELEASED]
switch from grouped data in category sales to line level. add group by in query instead
signed and unsigned template mapping complete, added as attribute to customers table
arrange category_sales data to be inputted into report
SQL query of data to be inputted complete
load of category_sales data into persistent duckdb
safe read of network file

[UNRELEASED]
- Automatic refresh of customer benefits
- convert into smaller pipelines. 
    1. prepare sales data and load into duckdb
    2. generate status reports
    3. generate QBRs (same data set)

[SMELLS]
little bit of arguement soup going on. lots of passing of conn, and yaml configs


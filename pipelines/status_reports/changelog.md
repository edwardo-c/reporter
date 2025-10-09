[RELEASED]
arrange category_sales data to be inputted into report
current and previous year query scaffold started
load of category_sales data into persistent duckdb
safe read of network file

[UNRELEASED]
mapping of signed vs unsigned customers - dictates which template to use
.duckdb table for customers: account_number(varchar) | report_type(varchar) | signed(bool)
join Customers to sales data
Refactor: One global getenv call

[SMELLS]
little bit of arguement soup going on. lots of passing of conn, and yaml configs


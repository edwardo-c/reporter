[RELEASED]
current and previous year query scaffold started
load of category_sales data into persistent duckdb
safe read of network file

[UNRELEASED]
func: takes table and report_map, merges values to map
arrange category_sales data to be inputted into report
.duckdb table for customers: account_number(varchar) | report_type(varchar) | signed(bool)
join Customers to sales data
Refactor: One global getenv call
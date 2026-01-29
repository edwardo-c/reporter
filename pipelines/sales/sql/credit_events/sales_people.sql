CREATE OR REPLACE TEMP TABLE sales_people AS 
SELECT DISTINCT 
  "Full Name" AS FullName, 
  "POS SalesPerson" AS PosID, 
  ID AS AcuID
FROM raw_sales_people
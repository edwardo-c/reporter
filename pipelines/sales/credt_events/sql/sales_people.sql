CREATE OR REPLACE TEMP TABLE sales_people AS 
SELECT DISTINCT 
  FullName, 
  PosID, 
  AcuID,
  Director,
FROM raw_sales_people
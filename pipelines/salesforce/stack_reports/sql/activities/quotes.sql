CREATE OR REPLACE TEMP VIEW new_quotes AS  
SELECT 
  CUST_CREATED_NAME AS SalesRep,
  'Created Quote' AS CreditType,
  CUST_CREATED_DATE AS ActivityDate,
  CDF1 AS ActivityScore,
  CUST_ID AS ActivityID
FROM raw_new_quotes
CREATE OR REPLACE TEMP VIEW new_accts AS  
SELECT 
  CREATED AS SalesRep,
  'Created Account' AS CreditType,
  CREATED_DATE AS ActivityDate,
  CDF1 AS ActivityScore,
  ACCOUNT_ID AS ActivityID
FROM raw_new_accts;
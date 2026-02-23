CREATE OR REPLACE TEMP VIEW new_calls AS 
SELECT 
  CREATED_BY AS SalesRep,
  ACTIVITY_ID AS ActivityID,
  CREATED_DATE AS ActivityDate,
  CDF1 AS ActivityScore,
  'Logged Call' AS CreditType
FROM raw_calls
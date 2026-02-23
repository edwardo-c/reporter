CREATE OR REPLACE TEMP VIEW new_opps AS  
SELECT 
  FULL_NAME AS SalesRep,
  'Created Opportunity' AS CreditType,
  CREATED_DATE AS ActivityDate,
  CDF1 AS ActivityScore,
  OPPORTUNITY_ID AS ActivityID
FROM raw_new_opps
CREATE OR REPLACE TEMP VIEW new_leads AS 
SELECT 
  LEAD_OWNER AS SalesRep,
  LEAD_ID AS ActivityID,
  CONVERTED_DATE AS ActivityDate,
  CDF1 AS ActivityScore,
  'Converted Lead' AS CreditType
FROM raw_converted_leads
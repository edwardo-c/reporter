CREATE OR REPLACE TEMP VIEW new_contacts AS 
SELECT 
  CONTACT_CREATED AS SalesRep,
  CONTACT_ID AS ActivityID,
  CREATED_DATE AS ActivityDate,
  CDF1 AS ActivityScore,
  'Created Contact' AS CreditType
FROM raw_new_contacts
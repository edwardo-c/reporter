CREATE OR REPLACE TEMP VIEW new_emails AS 
SELECT 
  OwnerId AS SalesRepID18,
  'EMAIL' AS ActivityCode,
  ActivityDate
FROM raw_emails
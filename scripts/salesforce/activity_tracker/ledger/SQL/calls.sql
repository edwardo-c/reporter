CREATE OR REPLACE TEMP VIEW new_calls AS 
SELECT 
  OwnerId AS SalesRepID18,
  'CALL' AS ActivityCode,
  ActivityDate AS ActivityDate
FROM raw_calls
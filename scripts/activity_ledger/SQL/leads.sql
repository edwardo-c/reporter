CREATE OR REPLACE TEMP VIEW new_leads AS 
SELECT 
  OwnerId AS SalesRepID18,
  'LEAD' AS ActivityCode,
  ConvertedDate AS ActivityDate
FROM raw_converted_leads
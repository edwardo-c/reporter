CREATE OR REPLACE TEMP VIEW new_quotes AS  
SELECT 
  CreatedById AS SalesRepID18,
  'QUOTE' AS ActivityCode,
  Date_Created__c AS ActivityDate
FROM raw_new_quotes
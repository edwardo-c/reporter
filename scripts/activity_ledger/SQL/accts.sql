CREATE OR REPLACE TEMP VIEW new_accts AS  
SELECT 
  CreatedById AS SalesRepID18,
  'ACCT' AS ActivityCode,
  CreatedDate AS ActivityDate
FROM raw_new_accts;
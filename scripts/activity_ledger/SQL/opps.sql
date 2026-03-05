CREATE OR REPLACE TEMP VIEW new_opps AS  
SELECT 
  CreatedById AS SalesRepID18,
  'OPP' AS ActivityCode,
  CreatedDate AS ActivityDate
FROM raw_new_opps
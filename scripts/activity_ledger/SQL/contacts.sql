CREATE OR REPLACE TEMP VIEW new_contacts AS 
SELECT 
  CreatedById AS SalesRepID18,
  'CONTACT' AS ActivityCode,
  CreatedDate AS ActivityDate
FROM raw_new_contacts
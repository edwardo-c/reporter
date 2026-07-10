CREATE OR REPLACE TEMP VIEW new_events AS  
SELECT 
  r.OwnerID AS SalesRepID18,
  s.ActivityCode AS ActivityCode,
  r.ActivityDate AS ActivityDate
FROM raw_meeting_events r
INNER JOIN scoring s
  ON UPPER(LEFT(r.Location, 3)) = UPPER(s.ActivityCode)
WHERE LOWER(s.Type) = LOWER('in_person') 
  OR LOWER(s.Type) = LOWER('virtual')
  OR LOWER(s.type) = LOWER('so')

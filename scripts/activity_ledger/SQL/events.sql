CREATE OR REPLACE TEMP VIEW new_events AS  
SELECT 
  r.OwnerID AS SalesRepID18,
  s.ActivityCode AS ActivityCode,
  r.ActivityDate AS ActivityDate
FROM raw_meeting_events r
INNER JOIN scoring s
  ON UPPER(LEFT(r.Location, 3)) = UPPER(s.ActivityCode)
WHERE LOWER(s.category) = 'event'
-- match to predefined meeting codes, 
-- business rule: place meeting code as first three letters of location field
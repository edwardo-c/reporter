CREATE OR REPLACE TEMP VIEW new_events AS  
WITH meeting_scores(meeting_code, score) AS (
    VALUES
        ('Z01', 5),  -- Virtual Project Meeting
        ('Z02', 5),  -- Virtual Training 
        ('X01', 10), -- In-Person QBR 
        ('X02', 10), -- In-Person Training 
        ('X03', 10)  -- In-Person Engagement 
)
SELECT 
  r.ASSIGNED AS SalesRep,
  'Event' AS CreditType,
  DUE_DATE AS ActivityDate,
  UPPER(LEFT("Location", 3)) AS MeetingCode, -- extract meeting code from location
  ms.score AS ActivityScore,
  ACTIVITY_ID AS ActivityID
FROM raw_meeting_events r
INNER JOIN meeting_scores ms
  ON UPPER(LEFT(r."Location", 3)) = ms.meeting_code
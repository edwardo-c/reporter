CREATE TEMP TABLE final_payload (
    Sales_Rep__c              VARCHAR NOT NULL,
    Period_Start__c           DATE NOT NULL,
    Period_Type__c            VARCHAR NOT NULL,
    Type__c                   VARCHAR NOT NULL,
    Sub_Type__c               VARCHAR NOT NULL,
    Activity__c               VARCHAR NOT NULL,
    External_ID__c            VARCHAR NOT NULL,
    Activity_Count__c         INTEGER NOT NULL,
    Activity_Score__c         INTEGER NOT NULL,
    
    
    PRIMARY KEY (
        Sales_Rep__c, 
        Period_Start__c, 
        Period_Type__c, 
        Type__c, 
        Sub_Type__c,
        Activity__c
    )
);

INSERT INTO final_payload
with max_score AS (
SELECT
    ActivityCode,
    ScoreCap
FROM scoring
), calculated AS (
SELECT
    ledger.SalesRepID18,
    ledger.ActivityCode,
    DATE_TRUNC('month', ledger.ActivityDate) AS ActivityDate,
    s.Type,
    s.SubType,
    s.Activity,
    COUNT(*) AS ActivityCount,
    SUM(s.Score) AS ActivityScore
FROM ActivityLedger ledger
LEFT JOIN scoring s
  ON ledger.ActivityCode = s.ActivityCode
GROUP BY 1, 2, 3, 4, 5, 6
)
SELECT
  c.SalesRepID18 AS Sales_Rep__c,
  c.ActivityDate AS Period_Start__c,
  'Monthly' AS Period_Type__c,
  c.Type AS Type__c,
  c.SubType AS Sub_Type__c,
  c.Activity AS Activity__c,
  
  concat_ws(
    '|',
    c.SalesRepID18,
    c.ActivityDate,
    'Monthly',
    c.Type,
    c.SubType,
    c.Activity
  ) AS External_ID__c,

  c.ActivityCount AS Activity_Count__c,

  CASE
    WHEN ms.ScoreCap IS NULL THEN c.ActivityScore
    ELSE LEAST(c.ActivityScore, ms.ScoreCap)
  END AS Activity_Score__c

FROM calculated c
LEFT JOIN max_score ms
  ON c.ActivityCode = ms.ActivityCode
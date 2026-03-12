CREATE TEMP TABLE final_payload (
    Sales_Rep__c              VARCHAR NOT NULL,
    Period_Start__c           DATE NOT NULL,
    Period_Type__c            VARCHAR NOT NULL,
    Type__c                   VARCHAR NOT NULL,
    SubType__c                VARCHAR NOT NULL,
    Activity__c               VARCHAR NOT NULL,
    Activity_Count__c         INTEGER NOT NULL,
    Activity_Score__c         INTEGER NOT NULL,
    
    PRIMARY KEY (
        Sales_Rep__c, 
        Period_Start__c, 
        Period_Type__c, 
        Type__c, 
        SubType__c,
        Activity__c
    )
);

INSERT INTO final_payload
SELECT
    ledger.SalesRepID18 as Sales_Rep__c,
    DATE_TRUNC('month', ActivityDate) AS Period_Start__c,
    'Monthly' AS Period_Type__c,
    s.Type AS Type__c,
    s.SubType AS SubType__c,
    s.Activity AS Activity__c,
    COUNT(*) AS Activity_Count__c,
    SUM(s.Score) AS Activity_Score__c
FROM ActivityLedger ledger
LEFT JOIN scoring s
  ON ledger.ActivityCode = s.ActivityCode
GROUP BY 1, 2, 3, 4, 5, 6
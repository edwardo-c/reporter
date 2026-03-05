CREATE OR REPLACE TEMP VIEW enriched AS
SELECT 
  ledger.SalesRepID18 AS Sales_Rep__c,
  DATE_TRUNC('month', ledger.ActivityDate) AS Period_Start__c,
  'Monthly' AS Period_Type__c,
  
  SUM(s.Score) AS Total_Score__c,

  -- Virtual Events --
  SUM(
    CASE s.SubCategory 
      WHEN 'virtual' THEN s.Score 
      ELSE 0 
    END) AS Virtual_Events_Score__c, 

  SUM(
    CASE s.SubCategory 
      WHEN 'virtual' THEN 1 
      ELSE 0 
    END) AS Virtual_Events_Count__c,

  -- in person events --
  SUM(
    CASE s.SubCategory 
      WHEN 'in_person' THEN s.Score 
      ELSE 0 
    END) AS In_Person_Events_Score__c, 

  SUM(
    CASE s.SubCategory 
      WHEN 'in_person' THEN 1 
      ELSE 0 
    END) AS In_Person_Events_Count__c,

  -- Contacts --
  SUM(
    CASE s.ActivityCode 
      WHEN 'CONTACT' THEN s.Score 
      ELSE 0 
    END) AS Contacts_Score__c, 

  SUM(
    CASE s.ActivityCode
      WHEN 'CONTACT' THEN 1 
      ELSE 0 
    END) AS Contacts_Count__c,

  -- Quotes --
  SUM(
    CASE s.ActivityCode 
      WHEN 'QUOTE' THEN s.Score 
      ELSE 0 
    END) AS Quotes_Score__c, 

  SUM(
    CASE s.ActivityCode  
      WHEN 'QUOTE' THEN 1 
      ELSE 0 
    END) AS Quotes_Count__c,

  -- Calls --
  SUM(
    CASE s.ActivityCode  
      WHEN 'CALL' THEN s.Score 
      ELSE 0 
    END) AS Calls_Score__c, 

  SUM(
    CASE s.ActivityCode 
      WHEN 'CALL' THEN 1 
      ELSE 0 
    END) AS Calls_Count__c,

  -- Converted Lead --
  SUM(
    CASE s.ActivityCode  
      WHEN 'LEAD' THEN s.Score 
      ELSE 0 
    END) AS Converted_Leads_Score__c, 

  SUM(
    CASE s.ActivityCode  
      WHEN 'LEAD' THEN 1 
      ELSE 0 
    END) AS Converted_Leads_Count__c,

  -- Created Account --
  SUM(
    CASE s.ActivityCode  
      WHEN 'ACCT' THEN s.Score 
      ELSE 0 
    END) AS Created_Accounts_Score__c, 

  SUM(
    CASE s.ActivityCode 
      WHEN 'ACCT' THEN 1 
      ELSE 0 
    END) AS Created_Accounts_Count__c,

  -- Created Opportunity --
  SUM(
    CASE s.ActivityCode 
      WHEN 'OPP' THEN s.Score 
      ELSE 0 
    END) AS Created_Opportunities_Score__c, 

  SUM(
    CASE s.ActivityCode  
      WHEN 'OPP' THEN 1 
      ELSE 0 
    END) AS Created_Opportunities_Count__c

FROM ActivityLedger ledger
LEFT JOIN scoring s
  ON ledger.ActivityCode = s.ActivityCode
GROUP BY SalesRepID18, DATE_TRUNC('month', ledger.ActivityDate)
CREATE OR REPLACE TEMP VIEW enriched AS
SELECT 
  SUBSTR(ledger.SalesRep, 1, 15) AS SalesRepId15,
  sp.FIRST_NAME || ' ' || sp.LAST_NAME AS FullName,
  ledger.CreditType,
  ledger.ActivityDate,
  ledger.ActivityScore,
  SUBSTR(ledger.ActivityID, 1, 15) AS ActivityID15
FROM ActivityLedger ledger
LEFT JOIN sales_people sp
  ON SUBSTR(ledger.SalesRep, 1, 15) = sp.USER_ID
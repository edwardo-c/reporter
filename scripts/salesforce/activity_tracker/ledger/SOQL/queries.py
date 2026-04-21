from scripts.salesforce.activity_tracker.ledger.SOQL.registry import register_query

EVENTS = """
SELECT 
  OwnerId,
  ActivityDate,
  Location
FROM Event
WHERE ActivityDate >= 2026-01-01 
  AND ActivityDate <= THIS_MONTH
"""
register_query("events", EVENTS)

CONTACTS = """
SELECT 
  CreatedById,
  CreatedDate 
FROM Contact
WHERE CreatedDate = THIS_YEAR
"""
register_query("contacts", CONTACTS)

OPPS = """
SELECT 
  CreatedById,
  CreatedDate 
FROM Opportunity
WHERE CreatedDate = THIS_YEAR
"""
register_query("opportunities", OPPS)

ACCTS = """
SELECT 
  CreatedById,
  CreatedDate 
FROM Account
WHERE CreatedDate = THIS_YEAR
"""
register_query("accounts", ACCTS)

QUOTES = """
SELECT 
  CreatedById,
  Date_Created__c 
FROM SBQQ__Quote__c
WHERE CreatedDate = THIS_YEAR
"""
register_query("quotes", QUOTES)

LEADS = """
SELECT 
  OwnerId,
  ConvertedDate 
FROM Lead 
WHERE IsConverted = True 
AND ConvertedDate = THIS_YEAR
"""
register_query("leads", LEADS)

CALLS = """
SELECT 
  OwnerId,
  ActivityDate
FROM Task
WHERE 
  TaskSubtype = 'Call' 
  AND ActivityDate = THIS_YEAR
"""
register_query("calls", CALLS)

EMAILS = """
SELECT 
  OwnerId, 
  ActivityDate 
FROM Task
WHERE 
  TaskSubtype = 'Email' 
  AND ActivityDate = THIS_YEAR
"""
register_query("emails", CALLS)
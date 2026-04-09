EXTERNAL_CONTACTS_SOQL = """
SELECT 
  Account.ACU_CUSTOMER_ID__c,
  Email
FROM Contact
WHERE (
  Receives_Pricing__c=True
  AND Account.Price_List_Delivery_to_Salesperson__c=null
  AND (Account.ACU_CUSTOMER_ID__c!=null OR Account.ACU_CUSTOMER_ID__c!='')
  AND (Email!=null OR Email!='')
  AND (Contact_Status__c='Active' OR Contact_Status__c=null)
)
"""

INTERNAL_CONTACTS_SOQL = """
SELECT 
  ACU_CUSTOMER_ID__c,
  Price_List_Delivery_to_Salesperson__r.Email
FROM Account
WHERE 
  Price_List_Delivery_to_Salesperson__c != NULL
  AND ACU_CUSTOMER_ID__c != NULL
"""
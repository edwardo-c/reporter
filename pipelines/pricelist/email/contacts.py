"""SOQL queries to return Internal and External price list recipient contact information"""

from utils.salesforce import run_SOQL

def get_contacts(auth: dict) -> dict[str, list]:
    """
    queries salesforce for internal and external price list recipients
    """
    internal, external = run_SOQL(auth=auth, query=[INTERNAL_CONTACTS_QUERY, EXTERNAL_CONTACTS_QUERY], df=False)

    out = {}

    # the queries used guarantee account numbers in external will NOT be 
    # in internal, therefore no code created to manage overwrite of acu_id
    # also, sf only allows one email addres for internal, therefore no 
    # list comprehension like in external

    for acct in external:
        acu_id  = acct.get("ACU_CUSTOMER_ID__c")
        contacts = acct["Contacts"]["records"] if "Contacts" in acct else []
        emails = [c["Email"] for c in contacts if c.get("Email")]
        out[acu_id] = emails

    for r in internal:
        acu_id = r.get("ACU_CUSTOMER_ID__c")
        email = list(r["Price_List_Delivery_to_Salesperson__r"]["Email"])
        out[acu_id] = email

    return out
    

""" 
    Returns the raw query string to External Contacts: 
    1. Contact has Recieves Price List checked
    2. active = true
    3. Account (Parent) has an acumatica ID
    4. Account (Parent) price list delivery to salesperson = NULL
"""
EXTERNAL_CONTACTS_QUERY = """ 
SELECT 
Id, ACU_CUSTOMER_ID__c,
    (
        SELECT ID, Name, Email 
        FROM Contacts
        WHERE (
            Receives_Pricing__c = true
            AND Email != NULL 
            AND (Contact_Status__c != 'Inactive' OR Contact_Status__c != NULL)
        )  
    )
FROM Account
WHERE (
    ACU_CUSTOMER_ID__c != NULL
    AND Price_List_Delivery_to_Salesperson__c = NULL
    AND Id IN (
        SELECT AccountID
        FROM Contact
        WHERE (
            Receives_Pricing__c = true
            AND Email != NULL 
            AND (Contact_Status__c != 'Inactive' OR Contact_Status__c != NULL)
        )
    )
)
"""


"""
    Returns raw string for Internal contacts query:
    1. Account has Acumatica ID
    2. Account has price list delivery to salesperson filled 
"""
INTERNAL_CONTACTS_QUERY = """
SELECT 
    ACU_Customer_ID__c,
    Price_List_Delivery_to_Salesperson__r.Email
FROM Account
WHERE 
    Price_List_Delivery_to_Salesperson__c != NULL
    AND ACU_Customer_ID__c != NULL
    AND Owner.Alias != 'EarlN'
"""
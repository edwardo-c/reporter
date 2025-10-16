"""SOQL queries to return Internal and External price list recipient contact information"""

def _external_contacts_query():
    """ 
    Returns the raw query string to External Contacts: 
    1. Contact has Recieves Price List checked
    2. active = true
    3. Account (Parent) has an acumatica ID
    4. Account (Parent) price list delivery to salesperson = NULL
    """
    
    return """ 
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

def _internal_contacts_query():
    """
    Returns raw string for Internal contacts query:
    1. Account has Acumatica ID
    2. Account has price list delivery to salesperson filled 
    """
    return """
        SELECT 
            ACU_Customer_ID__c,
            Price_List_Delivery_to_Salesperson__r.Email
        FROM Account
        WHERE 
            Price_List_Delivery_to_Salesperson__c != NULL
            AND ACU_Customer_ID__c !=NULL
        """
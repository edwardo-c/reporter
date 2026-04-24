CREATE OR REPLACE VIEW acu_base AS
SELECT
  TRIM(UPPER(CustID)) AS AcuId,
  TRIM(UPPER(PriceGroup)) AS PriceGroup,
  TRIM(UPPER(CustomerPriceClass)) AS CustPriceClass,
  UPPER(Trim(CustID) || '|' || TRIM(PriceGroup)) AS CustGroupKey,
  UPPER(
    TRIM(CustID) || '|' || TRIM(PriceGroup) || '|' || TRIM(CustomerPriceClass)
  ) AS CustGroupClassKey
FROM acu_cpg
;

CREATE OR REPLACE VIEW sf_base AS
SELECT
  TRIM(Id) AS Id18Char,
  TRIM(UPPER("Account__r.ACU_CUSTOMER_ID__c")) AS AcuId,
  TRIM(UPPER("Price_List__r.Sales_Price_Group__r.Name")) AS PriceGroup,
  TRIM(UPPER("Price_List__r.Customer_Price_Class__c")) AS CustPriceClass,
  UPPER(
    TRIM("Account__r.ACU_CUSTOMER_ID__c") || '|' ||
    TRIM("Price_List__r.Sales_Price_Group__r.Name") || '|' ||
    TRIM("Price_List__r.Customer_Price_Class__c")
  ) AS CustGroupClassKey,
  UPPER(
    TRIM("Account__r.ACU_CUSTOMER_ID__c") || '|' || 
    TRIM("Price_List__r.Sales_Price_Group__r.Name")
  ) AS CustGroupKey
FROM sf_cpg
;

-- updates can only happen to those customers that exist in both
CREATE OR REPLACE VIEW candidates AS
SELECT DISTINCT AcuId FROM acu_base
INTERSECT
SELECT DISTINCT AcuId FROM sf_base
;

CREATE OR REPLACE VIEW new_keys AS 
-- the Cust|Group|Class-Key in ACU not in SF
WITH base AS (
SELECT 
  DISTINCT ab.CustGroupClassKey 
FROM acu_base ab
JOIN candidates c
  ON ab.AcuId = c.AcuId
EXCEPT
SELECT
  DISTINCT sb.CustGroupClassKey
FROM sf_base sb
JOIN candidates c
  ON sb.AcuId = c.AcuId
)
SELECT 
  ab.AcuId,
  ab.PriceGroup,
  ab.CustPriceClass,
  'Add' AS "Action"
FROM base b
JOIN acu_base ab ON
  b.CustGroupClassKey = ab.CustGroupClassKey
;

CREATE OR REPLACE VIEW remove_keys AS
WITH base AS (
-- the Cust|Group|Class-Key in SF not in ACU
SELECT
  DISTINCT sb.CustGroupClassKey
FROM sf_base sb
JOIN candidates c
  ON sb.AcuId = c.AcuId
EXCEPT
SELECT 
  DISTINCT ab.CustGroupClassKey 
FROM acu_base ab
JOIN candidates c
  ON ab.AcuId = c.AcuId
)
SELECT
  sb.AcuId,
  sb.PriceGroup,
  sb.CustPriceClass,
  'Remove' AS "Action"
FROM base b
JOIN sf_base sb 
  ON b.CustGroupClassKey = sb.CustGroupClassKey
;

CREATE OR REPLACE VIEW audited_cpg AS
WITH base AS (
SELECT * FROM new_keys
UNION ALL
SELECT * FROM remove_keys
) 
SELECT * FROM base ORDER BY AcuId
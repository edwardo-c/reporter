CREATE OR REPLACE VIEW acu_base AS
SELECT
  "CleanedPartNumber" AS PartNumber,
  "ItemStatus" AS ItemStatus,
  "PriceGroup" AS PriceGroup,
  "Category" AS Category,
  "ProductLifeCycleManagement" AS PMPLCM,
  "CleanedAuthRequired" AS AuthRequired
FROM acu_products
;

CREATE OR REPLACE VIEW sf_base AS
SELECT
  TRIM(UPPER("Name")) AS PartNumber,
  TRIM(UPPER("ACU_Item_Status__c")) AS ItemStatus,
  TRIM(UPPER("Price_Group__r.Name")) AS PriceGroup,
  TRIM(UPPER("Category__c")) AS Category,
  TRIM(UPPER("ACU_PMPLCM__c")) AS PMPLCM,
  TRIM(UPPER("Auth_Required__c")) AS AuthRequired
FROM sf_products
;

CREATE OR REPLACE VIEW missing_in_sf AS
SELECT DISTINCT PartNumber FROM acu_base
EXCEPT
SELECT DISTINCT PartNumber FROM sf_base
;

CREATE OR REPLACE VIEW duplicates_in_sf AS
SELECT 
  PartNumber
FROM sf_base
GROUP BY PartNumber
HAVING COUNT(*) > 1;
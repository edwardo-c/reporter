CREATE OR REPLACE VIEW acu_base AS
SELECT
  "Normalized_PartNumber" AS PartNumber,
  TRIM("ItemStatus") AS ItemStatus,
  TRIM(UPPER("PriceGroup")) AS PriceGroup,
  TRIM("Category") AS Category,
  TRIM("ProductLifeCycleManagement") AS PMPLCM,
  TRIM(UPPER("Normalized_AuthRequired")) AS AuthRequired,
  SFIsActive AS SFIsActive,
  DEAL::DECIMAL(10,2) AS DEAL,
  PART::DECIMAL(10,2) AS PART,
  DIST::DECIMAL(10,2) AS DIST,
  SPEC::DECIMAL(10,2) AS SPEC,
  MSRP::DECIMAL(10,2) AS MSRP
FROM acu_products
;

CREATE OR REPLACE VIEW sf_base AS
WITH product_base  AS (
SELECT
  TRIM(UPPER("Name")) AS PartNumber,
  TRIM("ACU_Item_Status__c") AS ItemStatus,
  TRIM(UPPER("Price_Group__r.Name")) AS PriceGroup,
  TRIM("Category__c") AS Category,
  TRIM("ACU_PMPLCM__c") AS PMPLCM,
  TRIM(UPPER("Auth_Required__c")) AS AuthRequired,
  SF_IsActive__c AS SFIsActive
FROM sf_products
), price_levels AS (
SELECT
  TRIM(UPPER("Product__r.Name")) AS PartNumber,
  TRIM(UPPER("Price_List__r.Price_Group_Name__c")) AS PriceGroup,
  TRIM(UPPER("Price_List__r.Customer_Price_Class__c")) AS PriceClass,
  Price_List_Price__c::DECIMAL(10,2) AS Price
FROM sf_price_list_entries
), prices_levels_pivoted AS (
PIVOT price_levels 
ON PriceClass IN ('DEAL', 'PART', 'DIST', 'SPEC')
USING MAX(Price)
), msrp AS (
SELECT
  TRIM(UPPER("Product2.Name")) AS PartNumber,
  UnitPrice::DECIMAL(10,2) AS MSRP
FROM sf_msrp
)
SELECT 
  pb.PartNumber,
  plp.DEAL AS DEAL,
  plp.PART AS PART,
  plp.DIST AS DIST,
  plp.SPEC AS SPEC,
  m.MSRP AS MSRP,
  pb.ItemStatus,
  pb.PriceGroup,
  pb.Category,
  pb.PMPLCM,
  pb.AuthRequired,
  pb.SFIsActive
FROM product_base pb
LEFT JOIN prices_levels_pivoted plp
  ON pb.PartNumber = plp.PartNumber
LEFT JOIN msrp m
  ON pb.PartNumber = m.PartNumber
;

-- of the products that exist in acumatica, which do not have the correct fields?
CREATE OR REPLACE VIEW candidates AS
SELECT DISTINCT PartNumber FROM acu_base
INTERSECT
SELECT DISTINCT PartNumber FROM sf_base
;

CREATE OR REPLACE VIEW audited_products AS

WITH base AS (
SELECT
  c.PartNumber AS PartNumber,
  
  ab.SFIsActive AS acu_SFIsActive,
  sb.SFIsActive AS sf_SFIsActive,

  ab.ItemStatus AS acu_ItemStatus,
  sb.ItemStatus AS sf_ItemStatus,

  ab.PriceGroup AS acu_PriceGroup,
  sb.PriceGroup AS sf_PriceGroup,

  ab.Category AS acu_Category,
  sb.Category AS sf_Category,

  ab.PMPLCM AS acu_PMPLCM,
  sb.PMPLCM AS sf_PMPLCM,

  ab.AuthRequired AS acu_AuthRequired,
  sb.AuthRequired AS sf_AuthRequired,

  ab.DEAL AS acu_DEAL,
  sb.DEAL as sf_DEAL,

  ab.PART AS acu_PART,
  sb.PART as sf_PART,

  ab.DIST AS acu_DIST,
  sb.DIST as sf_DIST,

  ab.SPEC AS acu_SPEC,
  sb.SPEC as sf_SPEC,

  ab.MSRP AS acu_MSRP,
  sb.MSRP AS sf_MSRP

FROM acu_base ab
JOIN candidates c
  ON ab.PartNumber = c.PartNumber
JOIN sf_base sb
  ON sb.PartNumber = c.PartNumber
)

-- attribute check

SELECT
  b.PartNumber,
  'Active' AS AttributeToChange,
  b.acu_SFIsActive AS Acu_Value,
  b.sf_SFIsActive AS SF_Value
FROM base b
WHERE b.acu_SFIsActive IS DISTINCT FROM b.sf_SFIsActive

UNION ALL

SELECT
  b.PartNumber,
  'ACU Item Status' AS AttributeToChange,
  b.acu_ItemStatus AS Acu_Value,
  b.sf_ItemStatus AS SF_Value
FROM base b
WHERE b.acu_ItemStatus IS DISTINCT FROM b.sf_ItemStatus

UNION ALL

SELECT
  b.PartNumber,
  'US Price Group' AS AttributeToChange,
  b.acu_PriceGroup AS Acu_Value,
  b.sf_PriceGroup AS SF_Value
FROM base b
WHERE b.acu_PriceGroup IS DISTINCT FROM b.sf_PriceGroup

UNION ALL

SELECT
  b.PartNumber,
  'Category' AS AttributeToChange,
  b.acu_Category AS Acu_Value,
  b.sf_Category AS SF_Value
FROM base b
WHERE b.acu_Category IS DISTINCT FROM b.sf_Category

UNION ALL

SELECT
  b.PartNumber,
  'ACU PMPLCM' AS AttributeToChange,
  b.acu_PMPLCM AS Acu_Value,
  b.sf_PMPLCM AS SF_Value
FROM base b
WHERE b.acu_PMPLCM IS DISTINCT FROM b.sf_PMPLCM

UNION ALL

SELECT
  b.PartNumber,
  'ACU Authorization Required' AS AttributeToChange,
  b.acu_AuthRequired AS Acu_Value,
  b.sf_AuthRequired AS SF_Value
FROM base b
WHERE b.acu_AuthRequired IS DISTINCT FROM b.sf_AuthRequired

UNION ALL

-- price check

SELECT
  b.PartNumber,
  'DEAL Price List Entry' AS AttributeToChange,
  b.acu_DEAL AS Acu_Value,
  b.sf_DEAL AS SF_Value
FROM base b
WHERE b.acu_DEAL IS DISTINCT FROM b.sf_DEAL
  AND b.acu_DEAL > 0

UNION ALL

SELECT
  b.PartNumber,
  'PART Price List Entry' AS AttributeToChange,
  b.acu_PART Acu_Value,
  b.sf_PART AS SF_Value
FROM base b
WHERE b.acu_PART IS DISTINCT FROM b.sf_PART
  AND b.acu_PART > 0

UNION ALL

SELECT
  b.PartNumber,
  'DIST Price List Entry' AS AttributeToChange,
  b.acu_DIST Acu_Value,
  b.sf_DIST AS SF_Value
FROM base b
WHERE b.acu_DIST IS DISTINCT FROM b.sf_DIST
  AND b.acu_DIST > 0

UNION ALL

SELECT
  b.PartNumber,
  'SPEC Price List Entry' AS AttributeToChange,
  b.acu_SPEC Acu_Value,
  b.sf_SPEC AS SF_Value
FROM base b
WHERE b.acu_SPEC IS DISTINCT FROM b.sf_SPEC
  AND b.acu_SPEC > 0

UNION ALL

SELECT
  b.PartNumber,
  'Standard Price Book' AS AttributeToChange,
  b.acu_MSRP AS Acu_Value,
  b.sf_MSRP AS SF_Value
FROM base b
WHERE b.acu_MSRP IS DISTINCT FROM b.sf_MSRP
  AND b.acu_MSRP > 0

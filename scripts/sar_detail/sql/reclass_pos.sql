CREATE OR REPLACE TEMP VIEW reclass_pos_logic AS
WITH base AS (
SELECT 
  Customer AS Distributor,
  SoldToName AS CustomerName,
  BillToCustomerState AS BillToState,
  BillToCustomerZip AS BillToZip,
  'reclass' AS PayStructure,
  'SalesPerson' AS AppliesToQuota, 
  Credit AS SalesRep,
  PiiPartNumber AS PartNumber,
  "Reclass Cat" AS ProductCategory,
  ShipQuantity AS Quantity,
  "Reclass $" AS ExtendedSaleAmount,
  SaleDate AS InvoiceDate,
  ShipToState,
  ShipToZip,
  EXTRACT(MONTH FROM PeriodDate) AS CreditMonth,
  EXTRACT(YEAR FROM PeriodDate) AS CreditYear,
  "SAR Month" AS CreditMonthName,
  -- both captured in base, only one used in output for positive and negative values
  CASE WHEN 
    Credit = 'Christina Martinez' THEN 'No Rep'
    ELSE Credit 
  END AS SubtractFrom,
  
  CASE WHEN 
    Reclass = 'Christina Martinez' THEN 'No Rep'
    ELSE Reclass
  END AS AddTo
FROM raw_reclass_pos
), variants AS (
SELECT 'positive' AS variant, 1 AS sign
  UNION ALL
SELECT 'negative' AS variant, -1 AS sign
), crossed AS (
SELECT 
  b.*,
  CASE v.variant
    WHEN 'positive' THEN b.AddTo
    WHEN 'negative' THEN b.SubtractFrom
  END AS SalesRep,
  (b.ExtendedSaleAmount * v.sign) AS ExtendedSaleAmount
FROM base b
CROSS JOIN variants v
)
SELECT 
  x.*,
  d.Director
FROM crossed x
LEFT JOIN directors d
  ON x.SalesRep = d.FullName
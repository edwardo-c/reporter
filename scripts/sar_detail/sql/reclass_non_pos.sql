CREATE OR REPLACE TEMP VIEW reclass_non_pos_logic AS
WITH base AS (
SELECT 
  'PavDirect' AS Distributor,
  Account AS AccountNumber,
  "Customer Name" AS CustomerName,
  "Customer State" AS BillToState,
  "Account Group" AS AccountGroup,
  
  'Reclass' AS PayStructure,

  'SalesPerson' AS RepType,

  "Inventory CD" AS PartNumber,
  "Reclass Cat" AS ProductCategory,
  "Description" AS ProductDescription,
  Qty AS Quantity,
  "Reclass $" AS ExtendedSaleAmount,
  "Order Number" AS OrderNumber,
  "Customer PO Number" AS PoNumber,
  "Invoice Date" AS InvoiceDate,
  "Ship To Address Line 1" AS ShipToLineOne,
  "Ship To City" AS ShipToCity,
  "Ship To State" AS ShipToState,
  "Ship To Zip Code" AS ShipToZip,
  EXTRACT(MONTH FROM "Invoice Date") AS CreditMonth,
  EXTRACT(YEAR FROM "Invoice Date") AS CreditYear,
  "SAR Month" AS CreditMonthName,
  -- both captured in base, only one used in output for positive and negative values
  CASE Credit 
    WHEN 'Christina Martinez' THEN 'No Rep'
    ELSE Credit 
  END AS SubtractFrom,
  
  CASE Reclass 
    WHEN 'Christina Martinez' THEN 'No Rep'
    ELSE Reclass
  END AS AddTo

FROM raw_reclass_non_pos
), variants AS (
  SELECT 'positive' AS variant, 1 AS sign
  UNION ALL
  SELECT 'negative' AS variant, -1 AS sign
), crossed AS (
SELECT 
  
  b.* EXCLUDE (b.ExtendedSaleAmount),

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


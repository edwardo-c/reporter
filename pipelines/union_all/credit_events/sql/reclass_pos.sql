CREATE OR REPLACE TEMP VIEW reclass_pos AS
WITH base AS (
SELECT 
  Customer AS Distributor,
  NULL AS AccountNumber,
  SoldToName AS CustomerName,
  BillToCustomerState AS BillToState,
  NULL AS BillToCity,
  BillToCustomerZip AS BillToZip,
  NULL AS AccountGroup,
  'reclass' AS PayStructure,
  'SalesPerson' AS AppliesToQuota, 
  Credit AS SalesRep,
  PiiPartNumber AS PartNumber,
  "Reclass Cat" AS ProductCategory,
  NULL AS ProductDescription,
  ShipQuantity AS Quantity,
  "Reclass $" AS ExtendedSaleAmount,
  NULL AS OrderNumber,
  NULL AS PoNumber,
  SaleDate AS InvoiceDate,
  NULL AS ShipToLineOne,
  NULL AS ShipToCity,
  ShipToState,
  ShipToZip,
  EXTRACT(MONTH FROM PeriodDate) AS CreditMonth,
  EXTRACT(YEAR FROM PeriodDate) AS CreditYear,
  "SAR Month" AS CreditMonthName,
  -- both captured in base, only one used in output for positive and negative values
  Credit AS SubtractFrom,
  Reclass AS AddTo
FROM raw_reclass_pos
),
-- removed and added back in to enforce strict column order for UNION ALL --
positive AS (
SELECT 
  Distributor,
  AccountNumber,
  CustomerName,
  BillToState,
  BillToCity,
  BillToZip,
  AccountGroup,
  PayStructure,
  AppliesToQuota,
  AddTo AS SalesRep,
  PartNumber,
  ProductCategory,
  ProductDescription,
  Quantity,
  ExtendedSaleAmount,
  OrderNumber,
  PoNumber,
  InvoiceDate,
  ShipToLineOne,
  ShipToCity,
  ShipToState,
  ShipToZip,
  CreditMonth,
  CreditYear,
  CreditMonthName
FROM base
), 
negative AS (
SELECT 
  Distributor,
  AccountNumber,
  CustomerName,
  BillToState,
  BillToCity,
  BillToZip,
  AccountGroup,
  PayStructure,
  AppliesToQuota,
  SubtractFrom AS SalesRep,
  PartNumber,
  ProductCategory,
  ProductDescription,
  Quantity,
  -ExtendedSaleAmount,
  OrderNumber,
  PoNumber,
  InvoiceDate,
  ShipToLineOne,
  ShipToCity,
  ShipToState,
  ShipToZip,
  CreditMonth,
  CreditYear,
  CreditMonthName 
FROM base
)
SELECT * FROM positive
UNION ALL
SELECT * FROM negative;
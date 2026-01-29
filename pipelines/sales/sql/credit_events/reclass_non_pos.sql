CREATE OR REPLACE TEMP VIEW reclass_non_pos AS
WITH base AS (
SELECT 
  'PavDirect' AS Distributor,
  Account AS AccountNumber,
  "Customer Name" AS CustomerName,
  "Customer State" AS BillToState,
  NULL AS BillToCity,
  NULL AS BillToZip,
  "Account Group" AS AccountGroup,
  'reclass' AS CreditType,
  "Inventory CD" AS PartNumber,
  "Reclass Cat" AS ProductCategory,
  Description AS ProductDescription,
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
  Credit AS SubtractFrom,
  Reclass AS AddTo
FROM raw_reclass_non_pos
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
  CreditType,
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
  CreditType,
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
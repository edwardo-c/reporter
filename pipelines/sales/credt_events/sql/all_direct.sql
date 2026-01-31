CREATE OR REPLACE TEMP VIEW all_direct AS 
WITH base AS (
SELECT
  'PavDirect' AS Distributor,
  Account AS AccountNumber,
  "Customer Name" AS CustomerName,
  "Customer State" AS BillToState,
  NULL AS BillToCity,
  NULL AS BillToZip,
  "Account Group" AS AccountGroup,
  Type AS PayStructure,
  "Inside Sales Salesperson" AS InsideSales,
  "Key Manager Salesperson" AS KeyManager,
  "Key Director Salesperson" AS KeyDirector,
  "Sales Operations Salesperson" AS SalesOperations,
  "Outside Rep Firm" AS OutsideRepFirm,
  "Inventory CD" AS PartNumber,
  "Classification(Sales Category)" AS ProductCategory,
  Description AS ProductDescription,
  Qty AS Quantity,
  Amount AS ExtendedSaleAmount,
  "Order Number" AS OrderNumber,
  "Customer PO Number" AS PoNumber,
  "Invoice Date" AS InvoiceDate,
  "Ship To Address Line 1" AS ShipToLineOne,
  "Ship To City" AS ShipToCity,
  "Ship To State" AS ShipToState,
  "Ship To Zip Code" AS ShipToZip,
  EXTRACT(MONTH FROM "Invoice Date") AS CreditMonth,
  EXTRACT(YEAR FROM "Invoice Date") AS CreditYear,
  MONTHNAME("Invoice Date") AS CreditMonthName
FROM raw_all_direct
), unpivoted AS (
UNPIVOT base
ON InsideSales, KeyManager, KeyDirector, SalesOperations, OutsideRepFirm
INTO 
  Name AppliesToQuota
  Value AcuID
)
SELECT 
  u.Distributor,
  u.AccountNumber,
  u.CustomerName,
  u.BillToState,
  u.BillToCity,
  u.BillToZip,
  u.AccountGroup,
  u.PayStructure,
  u.CreditType,
  sp.FullName AS SalesRep,
  u.PartNumber,
  u.ProductCategory, 
  u.ProductDescription,
  u.Quantity,
  u.ExtendedSaleAmount,
  u.OrderNumber,
  u.PoNumber,
  u.InvoiceDate,
  u.ShipToLineOne,
  u.ShipToCity,
  u.ShipToState,
  u.ShipToZip,
  u.CreditMonth,
  u.CreditYear,
  u.CreditMonthName  
FROM unpivoted u
LEFT JOIN sales_people sp 
  ON u.AcuID = sp.AcuID
WHERE u.AcuID IS NOT NULL AND u.AcuID <> '';
CREATE OR REPLACE TEMP VIEW all_direct_logic AS 
WITH base AS (
SELECT
  'PavDirect' AS Distributor,
  Account AS AccountNumber,
  "Customer Name" AS CustomerName,
  "Customer State" AS BillToState,
  "Account Group" AS AccountGroup,

  "Inside Sales Salesperson" AS InsideSales,
  "Key Director Salesperson" AS KeyDirector,
  "Sales Operations Salesperson" AS SalesOperations,
  "Outside Rep Firm" AS OutsideRepFirm,
  
  -- "Key Manager Salesperson" AS KeyManager,


  "Inventory CD" AS PartNumber,
  "Classification(Sales Category)" AS ProductCategory,
  "Description" AS ProductDescription,
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
ON InsideSales, KeyDirector, SalesOperations, OutsideRepFirm -- ,KeyManager
INTO 
  Name RepType
  Value AcuID
)
SELECT 
  u.* EXCLUDE (RepType),
  sp.FullName AS SalesRep,

  CASE 
    WHEN u.RepType IN ('KeyManager', 'KeyDirector') 
    THEN 'KeyAccount'
    ELSE u.RepType
  END AS RepType

FROM unpivoted u
LEFT JOIN sales_people sp 
  ON u.AcuID = sp.AcuID
WHERE u.AcuID IS NOT NULL AND u.AcuID <> '';
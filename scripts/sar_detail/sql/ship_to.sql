CREATE OR REPLACE TEMP VIEW ship_to_logic AS 
SELECT
  'PavDirect' AS Distributor,
  Account AS AccountNumber,
  "Customer Name" AS CustomerName,
  "Customer State" AS BillToState,
  "Account Group" AS AccountGroup,
  'Ship To' AS CreditType,
  'SalesPerson' AS AppliesToQuota,
  
  CASE Credit 
    WHEN 'Christina Martinez' THEN 'No Rep' 
    ELSE Credit 
  END AS SalesRep,
  
  d.Director AS Director,

  "Inventory CD" AS PartNumber,
  "Classification(Sales Category)" AS ProductCategory,
  "Tran Desc" AS ProductDescription,
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
FROM raw_ship_to r
LEFT JOIN directors d
  ON r.Credit = d.FullName
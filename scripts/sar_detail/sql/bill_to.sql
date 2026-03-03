CREATE OR REPLACE TEMP VIEW bill_to_logic AS
SELECT
  'PavDirect' AS Distributor,
  Account AS AccountNumber,
  "Customer Name" AS CustomerName,
  "Customer State" AS BillToState,
  "Account Group" AS AccountGroup,
  'Bill To' AS PayStructure,
  
  -- credit and credit oversight -- 
  CASE "Account Owner" 
    WHEN 'CM6746' THEN 'No Rep' 
    ELSE "Account Owner" 
  END AS SalesRepID,

  "Inside Sales Salesperson" AS InsideSalesID,
  "Key Manager Salesperson" AS KeyManagerID,
  "Key Director Salesperson" AS KeyDirectorID,
  "Sales Operations Salesperson" AS SalesOpsID,


  

  d.Director AS Director,
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
FROM raw_bill_to r
LEFT JOIN directors d
  ON r.Credit = d.FullName
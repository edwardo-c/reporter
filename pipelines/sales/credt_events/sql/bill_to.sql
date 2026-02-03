-- selects available columns for Canonical Schema from raw_bill_to --

-- TODO: CTE sales reps with a director, drop null rows, left join with base 
-- to add in a layer for JB and TY. make a mini view for it so you do not have to do the same where clause
-- three times, this keeps it consistent accross all joins. 




CREATE OR REPLACE TEMP VIEW bill_to_logic AS 
WITH directors AS (
  SELECT
    AcuID,
    Director
  FROM sales_people
  WHERE Director IS NOT NULL
) 
SELECT
  'PavDirect' AS Distributor,
  Account AS AccountNumber,
  "Customer Name" AS CustomerName,
  "Customer State" AS BillToState,
  "Account Group" AS AccountGroup,
  Type AS PayStructure,
  'SalesPerson' AS AppliesToQuota,
  Credit AS SalesRep,
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
FROM raw_bill_to;
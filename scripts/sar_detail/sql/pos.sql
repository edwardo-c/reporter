CREATE OR REPLACE TEMP VIEW pos_logic AS 
SELECT
  Customer AS Distributor,
  SoldToName AS CustomerName,
  BillToCustomerState AS BillToState,
  BillToCustomerZip AS BillToZip,
  'POS' AS PayStructure,

  CASE Credit 
    WHEN 'Christina Martinez' THEN 'No Rep' 
    ELSE Credit 
  END AS SalesRep,
  
  d.Director AS Director,
  PiiPartNumber AS PartNumber,
  PiiCategory AS ProductCategory,
  ShipQuantity AS Quantity,
  ExtendedSales AS ExtendedSaleAmount,
  SaleDate AS InvoiceDate,
  ShipToState,
  ShipToZip,
  EXTRACT(MONTH FROM PeriodDate) AS CreditMonth,
  EXTRACT(YEAR FROM PeriodDate) AS CreditYear,
  MONTHNAME(PeriodDate) AS CreditMonthName
FROM raw_pos r
LEFT JOIN directors d
  ON r.Credit = d.FullName

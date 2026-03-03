CREATE OR REPLACE TEMP VIEW pos_logic AS 
SELECT

  CASE Customer
    WHEN 'EXERTIS ALMO' THEN 'ALMO'
    ELSE Customer
  END AS Distributor,  
  
  SoldToName AS CustomerName,
  BillToCustomerState AS BillToState,
  BillToCustomerZip AS BillToZip,
  'POS' AS PayStructure,

  CASE Credit 
    WHEN 'Christina Martinez' THEN 'No Rep' 
    ELSE Credit 
  END AS SalesRep_FullName,
  s.AcuID AS SalesRepID, 

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
LEFT JOIN sales_people s
  ON r.Credit = s.FullName

CREATE OR REPLACE TEMP VIEW pos_2025_logic AS 
SELECT
  Customer AS Distributor,
  SoldToName AS "Customer Name",
  PiiPartNumber AS "Part Number",
  ShipQuantity AS Quantity,
  ExtendedSales AS "Extended Sales",
  ShipToState AS "Ship To State",
  PeriodDate AS "Period Date"
FROM pos_2025
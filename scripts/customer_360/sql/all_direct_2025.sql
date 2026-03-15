CREATE OR REPLACE TEMP VIEW all_direct_2025_logic AS 
SELECT
  'PAVDIRECT' AS Distributor,
  Account AS "Account Number",
  "Customer Name",
  "Inventory CD" AS "Part Number",
  Description AS "Part Description",
  Qty AS "Quantity",
  Amount AS "Extended Sales",
  "Order Number",
  LAST_DAY("Invoice Date") AS "Period Date",
  "Ship To State"
FROM all_direct_2025
CREATE OR REPLACE TEMP VIEW enriched AS
SELECT 
  s.Distributor,
  COALESCE(x.Parent, s."Customer Name") AS "Customer Name",
  s."Account Number",
  s."Part Number",
  s."Part Description",
  s.Quantity,
  s."Extended Sales",
  s."Order Number",
  s."Period Date",
  s."Ship To State"
FROM All_Sales s
LEFT JOIN xRef x
  ON s."Customer Name" = x.Child
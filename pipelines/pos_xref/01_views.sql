CREATE OR REPLACE VIEW pos_sales_core AS
SELECT
  SoldToName          AS ChildName,
  MAX(BillToCustomerState) AS BillToState,
  MAX(BillToCustomerZip)   AS BillToZip
FROM raw_pos_sales
WHERE SoldToName IS NOT NULL
  AND SoldToName <> ''
GROUP BY SoldToName;


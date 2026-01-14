CREATE OR REPLACE VIEW pos_sales_core AS
SELECT DISTINCT
  SoldToName          AS ChildName,
  BillToCustomerState AS BillToState,
  BillToCustomerZip   AS BillToZip
FROM raw_pos_sales
WHERE SoldToName IS NOT NULL
  AND SoldToName <> '';

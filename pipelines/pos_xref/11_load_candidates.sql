INSERT INTO candidates (ChildName, BillToState, BillToZip)
SELECT
  core.ChildName,
  core.BillToState,
  core.BillToZip
FROM pos_sales_core core
LEFT JOIN cross_reference x
  ON core.ChildName = x.ChildName
LEFT JOIN candidates c
  ON core.ChildName = c.ChildName
WHERE x.ChildName IS NULL
  AND c.ChildName IS NULL;
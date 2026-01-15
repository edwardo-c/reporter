INSERT INTO candidates (ChildName, BillToState, BillToZip)
SELECT
  s.ChildName,
  s.BillToState,
  s.BillToZip
FROM pos_sales_core s
LEFT JOIN cross_reference x
  ON s.ChildName = x.ChildName
LEFT JOIN candidates c
  ON s.ChildName = c.ChildName
WHERE x.ChildName IS NULL
  AND c.ChildName IS NULL;
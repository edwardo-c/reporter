BEGIN TRANSACTION;

INSERT INTO customers (ParentName, BillToState, BillToZip)
SELECT DISTINCT
  d.ParentName,
  d.BillToState,
  d.BillToZip
FROM decisions d
WHERE NOT EXISTS (
  SELECT 1
  FROM customers c
  WHERE c.ParentName = d.ParentName
);

INSERT INTO cross_reference (ParentName, ChildName)
SELECT DISTINCT
  d.ParentName,
  d.ChildName
FROM decisions d
WHERE NOT EXISTS (
  SELECT 1
  FROM cross_reference x
  WHERE x.ChildName = d.ChildName
);

DELETE FROM candidates c
USING decisions d
WHERE c.ChildName = d.ChildName;

COMMIT;
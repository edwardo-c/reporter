CREATE OR REPLACE TEMP VIEW sales_people AS 
SELECT DISTINCT 
  FullName, 
  PosID, 
  AcuID,
  Director
FROM raw_sales_people;

CREATE OR REPLACE TEMP VIEW directors AS
SELECT
  FullName,
  AcuID,
  Director
FROM sales_people
WHERE Director IS NOT NULL;
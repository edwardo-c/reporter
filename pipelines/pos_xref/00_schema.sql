CREATE TABLE customers (
  ParentName VARCHAR NOT NULL, 
  BillToState VARCHAR, 
  BillToZip VARCHAR,
  PRIMARY KEY (ParentName)
);

CREATE TABLE cross_reference (
  ParentName VARCHAR NOT NULL,
  ChildName VARCHAR NOT NULL,
  PRIMARY KEY(ChildName),
  FOREIGN KEY (ParentName) REFERENCES customers(ParentName)
);

-- names to be reviewed manually
CREATE TABLE candidates (
  ChildName VARCHAR NOT NULL,
  BillToState VARCHAR,
  BillToZip VARCHAR,
  CHECK (ChildName <> ''),
  PRIMARY KEY (ChildName)
);

CREATE TABLE raw_pos_sales (
  Customer              VARCHAR,
  SoldToName            VARCHAR,
  SaleDate              DATE,
  PiiPartNumber         VARCHAR,
  PiiCategory           VARCHAR,
  ShipQuantity          DOUBLE,
  ExtendedSales         DOUBLE,
  BillToCustomerZip     VARCHAR,
  BillToCustomerState   VARCHAR,
  SalesRep              VARCHAR,
  ShipToState           VARCHAR,
  ShipToZip             VARCHAR,
  SalesRepAssignedRule  VARCHAR,
  PeriodDate            DATE,
  BatchId               VARCHAR NOT NULL,
  LoadedAt              TIMESTAMP NOT NULL
);


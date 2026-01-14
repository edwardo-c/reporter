INSERT INTO raw_pos_sales
SELECT
  *,
  ? AS BatchId,
  NOW() AS LoadedAt
FROM read_csv_auto(?);

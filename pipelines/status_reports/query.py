"""Arrange category_sales table for acceptance into report structure"""

query = """
SELECT
  acct_num,
  SUM(CASE WHEN year = 2025 AND part_category = 'MOUNT' THEN total ELSE 0 END) AS current_year_mounts,
  SUM(CASE WHEN year = 2025 AND part_category = 'DVLED' THEN total ELSE 0 END) AS current_year_dvled,
  SUM(CASE WHEN year = 2025 AND part_category = 'TV' THEN total ELSE 0 END) as current_year_tech,
  SUM(CASE WHEN year = 2025 AND part_category = 'KIOSK' THEN total ELSE 0 END) AS current_year_kiosks,
  SUM(CASE WHEN year = 2024 AND part_category = 'MOUNT' THEN total ELSE 0 END) as previous_year_mounts,
  SUM(CASE WHEN year = 2024 AND part_category = 'DVLED' THEN total ELSE 0 END) as previous_year_dvled,
  SUM(CASE WHEN year = 2024 AND part_category = 'KIOSK' THEN total ELSE 0 END) as previous_year_kiosks,
  SUM(CASE WHEN year = 2024 AND part_category = 'TV' THEN total ELSE 0 END) AS previous_year_tech
FROM category_sales
GROUP BY acct_num
"""


"""Arrange category_sales table for acceptance into report structure"""

import pandas as pd

def get_data_map(conn: object, report_cfg: dict):
    df: pd.DataFrame = _query(conn=conn)

    report_map = _df_to_cfg(df, report_cfg)

    return report_map

def _df_to_cfg(df:pd.DataFrame, report_map: dict):

    df_dict = df.to_dict('records')

    result_map = {}
    record_map = {}
    for record in df_dict:
        for range, col in report_map.items():
            record_map[range] = record[col] 
        # add to result map with acct_num key
        result_map[record["acct_num"]] = record_map

    return result_map

def _query(conn: object):
    query = """
    WITH sales AS(
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
    )
    SELECT
      c.acct_num,
      c.level_one_mount_goal,
      c.level_one_tech_goal,
      c.level_one_kiosks_goal,
      c.level_one_dvled_goal,
      c.level_one_mount_percent,
      c.level_one_tech_percent,
      c.level_one_kiosks_percent,
      c.level_one_dvled_percent,
      c.level_two_mount_goal,
      c.level_two_tech_goal,
      c.level_two_kiosks_goal,	
      c.level_two_dvled_goal,
      c.level_two_mount_percent,
      c.level_two_tech_percent,
      c.level_two_kiosks_percent,
      c.level_two_dvled_percent,
      c.level_three_mount_goal,
      c.level_three_tech_goal,
      c.level_three_kiosks_goal,
      c.level_three_dvled_goal,
      c.level_three_mount_percent,
      c.level_three_tech_percent,
      c.level_three_kiosks_percent,
      c.level_three_dvled_percent,
      s.current_year_mounts,
      s.current_year_dvled,
      s.current_year_tech,
      s.current_year_kiosks,
      s.previous_year_mounts,
      s.previous_year_dvled,
      s.previous_year_kiosks,
      s.previous_year_tech
    FROM customers AS c
    JOIN sales AS s ON s.acct_num = c.acct_num
    """

    return conn.sql(query).df()
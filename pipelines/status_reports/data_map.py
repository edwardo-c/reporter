"""Arrange category_sales table for acceptance into report structure"""

import pandas as pd

def get_data_map(conn: object, report_cfg: dict, timeframe: str):
    """
    Primary runner for preparing data map {acct_num: {ExcelRange: Value}}
    
    args:

      conn: connection object to duckdb to pull data from
    
      report_cfg: map of cell {range: column_name} to pull value from
        cell_range is the range to paste the data to
        column_name is the column name to extract the data from
      
      default_values: default values to each cell map
    """

    df: pd.DataFrame = _query(conn=conn)

    report_map = _df_to_cfg(df, report_cfg, timeframe=timeframe)

    return report_map

def _df_to_cfg(df:pd.DataFrame, report_cfg: dict[str, str],
               timeframe: str) -> list[dict[str, dict[str, dict]]]:
    """
    Map keys from report_map to values of df using cols as intersect
    return {fileName: CellValueMap,}

    Example:
      df= {
        acct_num: [abc, def], 
        2025_Total: [123, 456]
      }

      report_map: {"A1": "2025_Total"}

      result: {
        'abc': {"A1": 123},
        'def': {"A1: 456},
      }
    """
    df_dict = df.to_dict('records')

    out = []
    default = {"E3": f"As of {timeframe}"}

    for record in df_dict:
        
        signed = bool(record["signed"])
 
        out_file_name = _gen_file_name(
            signed=signed,
            name = record["header"],
            timeframe=timeframe
        )

        record_map = {
          xl_range: (
              f"{record[col_name]} Program Funding Status" if (xl_range == "B1") and signed
              else f"DRAFT - {record[col_name]} Program Funding Status" if (xl_range == "B1") and not signed
              else record[col_name]
          )
          for xl_range, col_name in report_cfg.items()
        }

        record_map.update(default)

        entry = {
            'meta': {
                'out_file_name': out_file_name, 
                'signed': signed, 
                'acct_num': record["acct_num"]
            },
            'value_map': record_map}

        out.append(entry)

    return out

def _gen_file_name(signed: bool, name: str, timeframe: str) -> str:
    base_name = f"{name} Status Report - {timeframe}.xlsx"
    if not signed:
        return f"UNEXECUTED - {base_name}"
    else:
        return base_name

def _query(conn: object):
    query = """
    WITH category_sales AS (
      SELECT
        acct_num,
        SUM(CASE WHEN year = 2025 AND part_category = 'MOUNT' THEN amount ELSE 0 END) AS current_year_mounts,
        SUM(CASE WHEN year = 2025 AND part_category = 'DVLED' THEN amount ELSE 0 END) AS current_year_dvled,
        SUM(CASE WHEN year = 2025 AND part_category = 'TV'    THEN amount ELSE 0 END) AS current_year_tech,
        SUM(CASE WHEN year = 2025 AND part_category = 'KIOSK' THEN amount ELSE 0 END) AS current_year_kiosks,
        SUM(CASE WHEN year = 2024 AND part_category = 'MOUNT' THEN amount ELSE 0 END) AS previous_year_mounts,
        SUM(CASE WHEN year = 2024 AND part_category = 'DVLED' THEN amount ELSE 0 END) AS previous_year_dvled,
        SUM(CASE WHEN year = 2024 AND part_category = 'KIOSK' THEN amount ELSE 0 END) AS previous_year_kiosks,
        SUM(CASE WHEN year = 2024 AND part_category = 'TV'    THEN amount ELSE 0 END) AS previous_year_tech
      FROM sales
      WHERE year IN (2024, 2025)
        AND part_category IN ('MOUNT','DVLED','TV','KIOSK')
      GROUP BY acct_num
    )
    SELECT
      c.acct_num,
      c.header,
      c.signed,
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
      COALESCE(cs.current_year_mounts,   0) AS current_year_mounts,
      COALESCE(cs.current_year_dvled,    0) AS current_year_dvled,
      COALESCE(cs.current_year_tech,     0) AS current_year_tech,
      COALESCE(cs.current_year_kiosks,   0) AS current_year_kiosks,
      COALESCE(cs.previous_year_mounts,  0) AS previous_year_mounts,
      COALESCE(cs.previous_year_dvled,   0) AS previous_year_dvled,
      COALESCE(cs.previous_year_kiosks,  0) AS previous_year_kiosks,
      COALESCE(cs.previous_year_tech,    0) AS previous_year_tech
    FROM customers AS c
    LEFT JOIN category_sales AS cs
      ON cs.acct_num = c.acct_num;
    """

    return conn.sql(query).df()
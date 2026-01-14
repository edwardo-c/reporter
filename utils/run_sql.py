from pathlib import Path

def run_sql_file(conn, path):
    sql = Path(path).read_text()
    conn.execute(sql)

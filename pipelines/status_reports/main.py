"""Primary runner for status report pipeline"""

from pipelines.status_reports.sales_refresh import refresh_data

def main():
    refresh_data()

if __name__ == "__main__":
    main()


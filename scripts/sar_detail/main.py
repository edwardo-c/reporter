from scripts.sar_detail.loaders import load_sales_data_to_db
from dotenv import load_dotenv
from scripts.sar_detail.config import ENV_VAR_PATH

def main():

    load_dotenv(ENV_VAR_PATH)
    load_sales_data_to_db()
    
    # transform

    # load into file
    ...

if __name__ == "__main__":
    main()
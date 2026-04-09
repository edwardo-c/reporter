from dotenv import load_dotenv
from config.paths import PRICE_LIST_ENV
load_dotenv(PRICE_LIST_ENV)

from scripts.pricelist.emailer import config
from scripts.pricelist.emailer import builders
from scripts.pricelist.emailer.loaders import load_contacts_df, load_customers_df
from scripts.pricelist.emailer.mappers import build_contacts_map, build_attachment_map


#TODO: implement user input in yaml

def main():
    contacts_df = load_contacts_df(
        internal_query=config.INTERNAL_CONTACTS_QUERY, 
        external_query=config.EXTERNAL_CONTACTS_QUERY,
        context=builders.READER_CTX
    )

    customers_df = load_customers_df(config.CUSTOMERS_ODATA, builders.READER_CTX)

    contacts_map = build_contacts_map(
        contacts_df, 
        config.LoadersSchema.acu_id.value, 
        value_col=config.LoadersSchema.email.value
    )

    pav_attachment_map = build_attachment_map(
        src_dir=(
            builders
            .APP_DIR_PATH_BUILDER
            .build_pav_finished_lists_dir("April 2026")
        )
    )

    nep_attachment_map = build_attachment_map(
        src_dir=(
            builders
            .APP_DIR_PATH_BUILDER
            .build_nep_finished_lists_dir("April 2026")
        )
    )


    # assemble email objects

    # send all emails


if __name__ == "__main__":

    main()
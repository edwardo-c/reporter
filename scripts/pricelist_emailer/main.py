
from dotenv import load_dotenv
from config.paths import PRICE_LIST_ENV
from scripts.pricelist_emailer.loaders import load_contacts, PriceListDFContactsFrames
from scripts.pricelist_emailer import config

def main(
        pav_dir_name: str, 
        nep_dir_name: str
    ):

    load_dotenv(PRICE_LIST_ENV)

    from scripts.pricelist_emailer import builders

    # load contacts from sf
    contact_frames: PriceListDFContactsFrames = load_contacts(
        config.SF_QUERY_OBJS, context=builders.READER_CTX
    )

    # TODO: internal_df is not being cleaned yet, load contacts is NOT ready yet

    # build

    # shape data

    # assemble email objects

    # send all emails


if __name__ == "__main__":

    main(
        pav_dir_name="April", 
        nep_dir_name="April"
    )
from scripts.pricelist.emailer import config
from config.paths import PRICE_LIST_ENV
from scripts.pricelist.emailer.secrets import load_env_vars
from scripts.pricelist.path_manager.manager import PriceListPathManager
from scripts.pricelist.emailer.builders import get_reader_ctx
from scripts.pricelist.emailer.loaders import get_external_data
from scripts.pricelist.emailer.settings import load_app_settings
from scripts.pricelist.emailer.mappers import get_mappers
from scripts.pricelist.emailer.assemblers import assemble_outputs

def main():

    env_vars = load_env_vars(PRICE_LIST_ENV)

    path_manager = PriceListPathManager(env_vars.root, env_vars.yaml)

    app_settings = load_app_settings(path_manager)

    ctx = get_reader_ctx(env_vars)

    external_data = get_external_data(config.SOURCES, ctx)

    mappers = get_mappers(external_data, config.SOURCES, app_settings)

    output_resources = assemble_outputs(
        mappers, 
        app_settings, 
        config.RESULTS_LOG
    )

    breakpoint()

    """
    TODO: 
    fill email bodies
    send email bodies
    """


if __name__ == "__main__":
    main()
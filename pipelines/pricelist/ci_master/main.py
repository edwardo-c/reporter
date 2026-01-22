from dotenv import load_dotenv

import xlwings as xw

from config.paths import CI_PRICELIST_CFG, CI_PRICELIST_ENV_VARS
from data_toolkit.template_copier import TemplateCopier
from pipelines.pricelist.template_meta.pricelist_meta import MasterPriceListTemplateMeta
from utils.yaml_loader import load_yaml

from data_toolkit.xl_modifier.ops_resolver import resolve_op
from data_toolkit.xl_modifier.obj_resolver import ObjectResolver

def main():

    load_dotenv(CI_PRICELIST_ENV_VARS)
    cfg = load_yaml(CI_PRICELIST_CFG)

    tmplt_meta = MasterPriceListTemplateMeta()

    with xw.App(visible=True, add_book=False) as xl_app:

        for c in cfg:
            
            copier = TemplateCopier(**c["copier_args"])
            
            variants = c["variants"]
            
            for v in variants:
                
                copy = copier.write_copy(v["out_name"])

                wb = xl_app.books.open(copy)

                resolver = ObjectResolver(wb)

                steps = v["steps"]

                for step in steps:
                    
                    obj_target = step["obj_target"]

                    obj_address = getattr(tmplt_meta, obj_target)

                    xl_object = resolver.resolve(obj_address)

                    handler = resolve_op(step["op"])

                    handler(xl_object, **step["kwargs"])

                breakpoint()


if __name__ == "__main__":
    main()
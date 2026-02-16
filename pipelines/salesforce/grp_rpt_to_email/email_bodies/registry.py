from pipelines.salesforce.grp_rpt_to_email.email_bodies.bodies import overdue_opps_body

REGISTRY = {
    "overdue_opps": overdue_opps_body
}

def get_email_func(func_id: str):
    if func_id not in REGISTRY:
        raise KeyError(
            f"unexpected email function id, got {func_id}"
            f"available keys found in ..bodies.REGISTRY"
        )
    else:
        return REGISTRY[func_id]
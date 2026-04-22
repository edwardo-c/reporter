from scripts.salesforce.audit import cfg
from scripts.salesforce.audit.audit_obj import AuditObj

JOBS_REGISTRY = {
    "customer_price_groups": cfg.CPG_AUDIT_OBJ,
    "products": cfg.PRODUCT_AUDIT_OBJ,
}

OPTIONS = tuple(JOBS_REGISTRY.keys())

def get_job(job_name: str) -> AuditObj | None:
    _job_name = job_name.lower()
    if _job_name not in OPTIONS:
        raise ValueError(f"{job_name} is not a valid job name")
    return JOBS_REGISTRY.get(_job_name, None)
from scripts.salesforce.audit import cfg
from scripts.salesforce.audit.secrets import load_env_vars
from scripts.salesforce.audit.builders import get_reader_ctx
from utils.yaml_loader import load_yaml
from scripts.salesforce.audit.process import run_jobs

def main():

    env_vars = load_env_vars(cfg.ENV_VAR_PATH)
    ctx = get_reader_ctx(env_vars)
    jobs = load_yaml(cfg.YAML_SETTINGS_PATH)
    
    # too nested; need to bring out what is happening inside. 
    run_jobs(jobs, ctx)

if __name__ == "__main__":
    main()
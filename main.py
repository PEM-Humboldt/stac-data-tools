# docs/main.py
def define_env(env):
    """
    Called by mkdocs-macros-plugin at build time.
    We load docs/data/cli.yml and expose it as {{ cli }} in templates.
    """
    import os, yaml

    # YAML relative path
    yml_path = os.path.join(env.project_dir, "docs", "data", "cli.yml")

    with open(yml_path, "r", encoding="utf-8") as f:
        env.variables["cli"] = yaml.safe_load(f)

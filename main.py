import os, yaml
import json


def define_env(env):

    base_path = os.path.join(env.project_dir, "docs", "commands")

    @env.macro
    def command():
        """
        Returns the YAML corresponding to the current page name.
        """
        page_name = env.page.title.lower()

        yml_file = os.path.join(base_path, f"{page_name}.yml")

        if os.path.exists(yml_file):
            with open(yml_file, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        else:
            return {"error": f"{page_name}.yml doesn't exist"}

    @env.macro
    def render_json(filename):
        """
        Renders a JSON file as a markdown code block.
        """
        json_path = os.path.join(env.project_dir, "docs", filename)
        with open(json_path, "r", encoding="utf-8") as f:
            return f"```json\n{f.read()}\n```"

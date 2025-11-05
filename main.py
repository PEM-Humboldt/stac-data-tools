def define_env(env):

    import os, yaml

    base_path = os.path.join(env.project_dir, "docs", "commands")

    @env.macro
    def command():
        """
        Returns the YAML corresponding to the current page name.
        """
        # Obtener el nombre del archivo desde la URL de la página (más confiable que el título)
        # La URL será algo como "/add_item/" o "/add_item"
        page_url = env.page.url.strip("/")
        
        if page_url:
            # Extraer el nombre del archivo desde la URL (ej: "add_item/" -> "add_item")
            page_name = page_url.split("/")[-1]
            # Si el nombre tiene .md, removerlo
            if page_name.endswith(".md"):
                page_name = page_name[:-3]
        else:
            # Fallback: usar el título de la página si no hay URL
            page_name = env.page.title.lower().replace(" ", "_")

        yml_file = os.path.join(base_path, f"{page_name}.yml")

        if os.path.exists(yml_file):
            with open(yml_file, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        else:
            return {"error": f"{page_name}.yml doesn't exist"}

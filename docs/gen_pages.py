import os
import mkdocs_gen_files

template_path = os.path.join("docs", "command.md")

commands_dir = os.path.join("docs", "commands")

def gen_files():
    """
    Generate md files from yml files.
    """
    with open(template_path, "r", encoding="utf-8") as tpl:
        template_content = tpl.read()
    
    for fname in sorted(os.listdir(commands_dir)):
        if fname.endswith(".yml"):
            name = os.path.splitext(fname)[0]

            with mkdocs_gen_files.open(f"{name}.md", "w") as f:
                f.write(template_content)

gen_files()
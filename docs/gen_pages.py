import os
import mkdocs_gen_files

template_path = os.path.join("docs", "command.md")

commands_dir = os.path.join("docs", "commands")

summary_lines = ["- [Inicio](index.md)\n", "- Comandos\n"]

def gen_files():
    """
    Generate md files from yml files.
    """
    with open(template_path, "r", encoding="utf-8") as tpl:
        template_content = tpl.read()
    
    for fname in sorted(os.listdir(commands_dir)):
        if fname.endswith(".yml"):
            name = os.path.splitext(fname)[0]
            md_file = f"{name}.md"

            with mkdocs_gen_files.open(md_file, "w") as f:
                f.write(template_content)
            
            summary_lines.append(f"    - [{name.capitalize()}]({md_file})\n")

    with mkdocs_gen_files.open("summary.md", "w") as f:
        f.writelines(summary_lines)

gen_files()
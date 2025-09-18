#!/usr/bin/env python3
"""
generate_docs.py

Generates Markdown (DOCS_DIR/commands_info/*.md) for each CLI subcommand (argparse),
and appends extended information from `commands_extended/<cmd>.md` if it exists.
- Discovers commands automatically from `python src/main.py --help`.
- Extracts short description from the commands section.
- Extracts usage and options from `python src/main.py <cmd> --help`.
- Normalizes argparse-wrapped lines so options look clean.
"""

import sys
import subprocess
from pathlib import Path
import os
import re

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.config import get_settings

def load_env_config():
    """Load and validate environment configuration from src/config.py.
    
    Returns:
        tuple: (main_file_path, docs_dir_path)
        
    Raises:
        ValueError: If required paths are invalid
    """
    project_root = Path(__file__).resolve().parent.parent
    
    settings = get_settings()
    
    main_file_path = (project_root / settings.main_file).resolve()
    if not main_file_path.exists():
        raise ValueError(f"Main file not found at {main_file_path}")
    docs_dir_path = project_root / settings.docs_dir
    
    return main_file_path, docs_dir_path

try:
    MAIN_FILE, DOCS_BASE = load_env_config()
    MAIN_FILE_DISPLAY = os.path.relpath(MAIN_FILE, MAIN_FILE.parent.parent)
except ValueError as e:
    print(f"Configuration error: {e}", file=sys.stderr)
    sys.exit(1)

INFO_DIR = DOCS_BASE / "commands_info"
EXTENDED_DIR = DOCS_BASE / "commands_extended"
INFO_DIR.mkdir(parents=True, exist_ok=True)
EXTENDED_DIR.mkdir(parents=True, exist_ok=True)

INFO_DIR.mkdir(parents=True, exist_ok=True)
EXTENDED_DIR.mkdir(parents=True, exist_ok=True)

def run_help(cmd_args):
    """Execute main.py with help arguments and return the output.
    
    Args:
        cmd_args (list): Command arguments to pass to main.py
        
    Returns:
        str: Combined stdout and stderr output from the command
        
    Raises:
        subprocess.CalledProcessError: If the command fails to execute
    """
    if not MAIN_FILE.exists():
        raise FileNotFoundError(f"Main script not found at {MAIN_FILE}")
        
    env = {**os.environ, "PYTHONPATH": str(MAIN_FILE.parent)}
    try:
        proc = subprocess.run(
            [sys.executable, str(MAIN_FILE)] + cmd_args,
            capture_output=True,
            text=True,
            check=True,
            env=env,
        )
        return proc.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e.stderr}", file=sys.stderr)
        return e.stdout or e.stderr or ""

def get_commands_overview():
    """Extract commands and their descriptions from the main help output.
    
    Returns:
        dict: Mapping of command names to their descriptions
    """
    out = run_help(["--help"])
    overview = {}
    
    command_match = re.search(r'{([^}]+)}', out)
    if command_match:
        commands = [cmd.strip() for cmd in command_match.group(1).split(',')]
        
        current_cmd = None
        current_desc = []
        in_options = False
        
        for line in out.splitlines():
            line = line.strip()
            if not line:
                continue
            
            if line.lower() == 'options:':
                in_options = True
                continue
                
            if in_options:
                continue
                
            for cmd in commands:
                cmd = cmd.strip()
                if line.startswith(cmd + " "):
                    if current_cmd:
                        overview[current_cmd] = ' '.join(current_desc)
                    current_cmd = cmd
                    current_desc = [line[len(cmd):].strip()]
                    break
            else:
                if current_cmd and not line.startswith('-'):
                    current_desc.append(line)
        
        if current_cmd:
            overview[current_cmd] = ' '.join(current_desc)
    
    return overview

def clean_usage_text(usage):
    if not usage:
        return usage
    tokens = usage.split()
    if tokens and tokens[0].endswith("main.py"):
        tokens = tokens[1:]
    return " ".join(tokens)

def parse_help_text(help_text):
    usage = ""
    options = []
    lines = help_text.splitlines()

    for line in lines:
        m = re.match(r'^\s*usage:?\s*(.*)', line, flags=re.IGNORECASE)
        if m:
            usage = m.group(1).strip()
            break

    start_idx = None
    for i, line in enumerate(lines):
        if line.strip().lower() in ['optional arguments:', 'options:', 'positional arguments:']:
            continue
        if re.match(r'^\s*(optional arguments|options|positional arguments):', line, flags=re.IGNORECASE):
            start_idx = i + 1
            break

    if start_idx is None:
        for i, line in enumerate(lines):
            if re.match(r'^\s+-', line):
                start_idx = i
                break

    if start_idx is None:
        return usage, options

    current_flag = None
    current_desc = []

    for line in lines[start_idx:]:
        if re.match(r'^\s*[A-Za-z ]+:$', line) and not re.match(r'^\s+-', line):
            break

        if not line.strip():
            if current_flag:
                options.append((current_flag.strip(), " ".join(current_desc).strip()))
                current_flag, current_desc = None, []
            continue

        if line.lstrip().startswith("-"):
            if current_flag:
                options.append((current_flag.strip(), " ".join(current_desc).strip()))
                current_flag, current_desc = None, []

            raw = line.strip()
            parts = re.split(r'\s{2,}', raw, maxsplit=1)
            if len(parts) == 2:
                current_flag = parts[0].strip()
                current_desc = [parts[1].strip()]
            else:
                current_flag = raw
                current_desc = []
        else:
            if current_flag is not None:
                current_desc.append(line.strip())

    if current_flag:
        options.append((current_flag.strip(), " ".join(current_desc).strip()))

    return usage, options

commands_overview = get_commands_overview()
COMMANDS = [cmd for cmd in commands_overview.keys() 
           if cmd.isidentifier() and not cmd.endswith(':')]

for cmd in COMMANDS:
    help_text = run_help([cmd, "--help"])
    usage_raw, options = parse_help_text(help_text)
    usage = clean_usage_text(usage_raw)
    desc = commands_overview.get(cmd, "").strip() or "_No description found._"
    desc = desc.replace("<", "\\<").replace(">", "\\>")

    out_path = INFO_DIR / f"{cmd}.md"
    with out_path.open("w", encoding="utf-8") as fh:
        fh.write(f"# {cmd.capitalize()} Command\n\n")
        fh.write("## Description\n\n")
        fh.write(desc + "\n\n")

        if usage:
            fh.write("## Usage\n\n")
            fh.write("```bash\n")
            fh.write(f"python {MAIN_FILE_DISPLAY} {usage}\n")
            fh.write("```\n\n")

        fh.write("## Options\n\n")
        if options:
            for flag, opt_desc in options:
                if opt_desc:
                    fh.write(f"- `{flag}`  \n  {opt_desc}\n\n")
                else:
                    fh.write(f"- `{flag}`\n\n")
        else:
            fh.write("_No options found._\n\n")

        extended_file = EXTENDED_DIR / f"{cmd}.md"
        if extended_file.exists():
            fh.write("\n---\n\n")
            with extended_file.open("r", encoding="utf-8") as ef:
                fh.write(ef.read())

    print(f"[generate_docs] -> {out_path}")

print(f"[generate_docs] ✅ Done. Markdown generated under: {INFO_DIR.resolve()}")

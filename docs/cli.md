# STAC Collection Manager

```python exec="on" result="markdown" hide_code="on"
from cli import build_parser   # o: from stac_data_tools.cli import build_parser
import argparse, re

PROG = "sdt"

parser = build_parser()

def esc(s: str) -> str:
    return (s or "").replace("<","&lt;").replace(">","&gt;")

def normalize_usage(text: str) -> str:
    text = re.sub(r"\b__main__\.py\b", PROG, text.strip())
    text = re.sub(r"^\s*usage:\s*", "", text)
    return re.sub(r"\s+", " ", text)

def fence(text: str, lang: str = "bash"):
    print()
    print(f"```{lang}")
    print((text or "").rstrip("\n"))
    print("```")
    print()

def param_bullets(p):
    rows = []
    for a in p._actions:
        if isinstance(a, argparse._HelpAction): continue
        if isinstance(a, argparse._SubParsersAction): continue
        if not a.option_strings and a.dest == "command": continue
        name = ", ".join(a.option_strings) if a.option_strings else (a.metavar or a.dest)
        required = bool(getattr(a, "required", False) and a.option_strings)
        help_ = getattr(a, "help", "") or ""
        default = getattr(a, "default", None)
        if default not in (None, argparse.SUPPRESS, False):
            help_ = (help_ + f" (default: {default})").strip()
        req = "required" if required else "optional"
        rows.append(f"- `{esc(name)}` ({req}): {esc(help_)}")
    return rows

# Top description
if parser.description:
    print(esc(parser.description))
    print()

# Commands
sub = next((a for a in parser._actions if isinstance(a, argparse._SubParsersAction)), None)
if sub and getattr(sub, "choices", None):
    print("## Commands")
    for name, sp in sorted(sub.choices.items(), key=lambda kv: kv[0]):
        short = getattr(sp, "help", None)
        print(f"\n### {name}" + (f" — {esc(short)}" if short else "") + "\n")

        if sp.description:
            print(esc(sp.description))
            print()

        print("#### Usage")
        fence(normalize_usage(sp.format_usage()), "bash")

        bullets = param_bullets(sp)
        if bullets:
            print("#### Parameters\n")
            print("\n".join(bullets))
            print()
```

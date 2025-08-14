import shutil
import subprocess
import sys

COMMANDS = [
    [
        "autoflake",
        "--in-place",
        "--remove-unused-variables",
        "--remove-all-unused-imports",
        "-r",
        "src",
    ],
    ["isort", "src"],
    ["black", "src"],
    ["autopep8", "--in-place", "--aggressive", "--aggressive", "-r", "src"],
    ["flake8", "src"],
]


def check_installed(cmd):
    """Check if the command is available in the environment."""
    return shutil.which(cmd[0]) is not None


def run_commands():
    for cmd in COMMANDS:
        if not check_installed(cmd):
            print(
                f"❌ Comando no encontrado: {cmd[0]}. Instálalo en el entorno antes de continuar."
            )
            sys.exit(1)
        print(f"▶ Ejecutando: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
    print("✅ Formateo y linting completados.")


if __name__ == "__main__":
    run_commands()
